from typing import List, Optional, Dict, Any

from flask_jwt_extended import current_user

from backend.extensions import casbin_enforcer
from backend.user.domain.permission import Permission
from backend.user.repository.permission.sqla import PermissionRepository
from backend.user.message import PERMISSION_HAS_CHILDREN, PERMISSION_IN_USE
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService
from kit.util import casbin as casbin_util

__all__ = ['PermissionService']


class PermissionService(CRUDService[Permission]):
    """权限服务实现"""

    def create(self, permission: Permission) -> Permission:
        """
        创建权限

        Args:
            permission: 权限对象

        Returns:
            创建后的权限对象
        """
        # 设置创建者
        permission.creator = current_user.username

        # 如果是子权限，需要确认父权限存在
        if permission.parent_id:
            parent = self.get(permission.parent_id)
            if not parent:
                raise ServiceBadRequest(f"父权限ID {permission.parent_id} 不存在")

        # 创建权限
        result = super().create(permission)

        # 如果有权限标识，添加到Casbin策略
        if permission.perms:
            # 注册资源到Casbin
            self._register_permission_resource(permission)

        return result

    def update(self, permission_id: int, permission: Permission) -> Optional[Permission]:
        """
        更新权限

        Args:
            permission_id: 权限ID
            permission: 更新的权限对象

        Returns:
            更新后的权限对象
        """
        # 设置修改者
        permission.modifier = current_user.username

        # 获取原有权限信息
        original = self.get(permission_id)
        if not original:
            return None

        # 如果权限标识发生变化，需要更新Casbin策略
        if original.perms != permission.perms:
            if original.perms:
                # 移除旧的资源权限
                self._remove_permission_resource(original)

            if permission.perms:
                # 添加新的资源权限
                self._register_permission_resource(permission)

        # 更新权限
        return super().update(permission_id, permission)

    def delete(self, permission_id: int) -> None:
        """
        删除权限

        Args:
            permission_id: 权限ID
        """
        # 获取权限信息
        permission = self.get(permission_id)
        if not permission:
            return

        # 检查是否有子权限
        children = self.repo.get_children(permission_id)
        if children:
            raise ServiceBadRequest(PERMISSION_HAS_CHILDREN)

        # 检查是否被角色使用
        is_used = self._check_permission_in_use(permission)
        if is_used:
            raise ServiceBadRequest(PERMISSION_IN_USE)

        # 如果有权限标识，从Casbin删除
        if permission.perms:
            self._remove_permission_resource(permission)

        # 逻辑删除权限
        self.repo.logical_delete(permission_id)

    def get_permission_tree(self) -> List[dict]:
        """
        获取权限树结构

        Returns:
            权限树结构
        """
        return self.repo.build_permission_tree()

    def get_menu_permissions(self) -> List[dict]:
        """
        获取菜单类型的权限树

        Returns:
            菜单权限树
        """
        # 获取所有菜单权限
        menu_permissions = self.repo.session.query(self.repo.model).filter(
            self.repo.model.menu_type == 0,
            self.repo.model.status == 1,
            self.repo.model.is_deleted == 0
        ).order_by(self.repo.model.level, self.repo.model.sort_order).all()

        # 构建层级结构
        menu_dict = {}
        menu_tree = []

        # 构建节点字典，方便查找
        for menu in menu_permissions:
            menu_dict[menu.id] = {
                'id': menu.id,
                'name': menu.name,
                'number': menu.number,
                'path': menu.path,
                'component': menu.component,
                'icon': menu.icon,
                'level': menu.level,
                'parent_id': menu.parent_id,
                'sort_order': menu.sort_order,
                'children': []
            }

        # 构建树结构
        for menu_id, menu_item in menu_dict.items():
            if menu_item['parent_id'] is None:
                # 一级菜单
                menu_tree.append(menu_item)
            else:
                # 子菜单，添加到父菜单的children中
                parent_id = menu_item['parent_id']
                if parent_id in menu_dict:
                    menu_dict[parent_id]['children'].append(menu_item)

        return menu_tree

    def get_user_menus(self, username: str) -> List[dict]:
        """
        获取用户有权限访问的菜单

        Args:
            username: 用户名

        Returns:
            用户有权限访问的菜单列表
        """
        # 获取所有菜单类型权限
        all_menus = self.get_menu_permissions()

        # 如果是管理员，返回所有菜单
        if username == 'admin':
            return all_menus

        # 获取用户角色的所有权限
        casbin_enforcer.e.load_policy()
        roles = casbin_enforcer.e.get_roles_for_user(username)

        user_permissions = set()
        for role in roles:
            # 获取角色的所有权限
            role_permissions = casbin_enforcer.e.get_permissions_for_user(role)
            for permission in role_permissions:
                if len(permission) >= 3:  # 确保权限格式正确
                    user_permissions.add(permission[1])  # 权限标识在第二个位置

        # 过滤出用户有权限的菜单
        return self._filter_user_menus(all_menus, user_permissions)

    def _filter_user_menus(self, menus: List[dict], user_permissions: set) -> List[dict]:
        """
        过滤用户有权限的菜单

        Args:
            menus: 所有菜单
            user_permissions: 用户拥有的权限标识集合

        Returns:
            过滤后的菜单列表
        """
        result = []
        for menu in menus:
            # 检查菜单权限
            if self._check_menu_permission(menu, user_permissions):
                # 递归处理子菜单
                if 'children' in menu and menu['children']:
                    filtered_children = self._filter_user_menus(menu['children'], user_permissions)
                    menu_copy = menu.copy()
                    menu_copy['children'] = filtered_children
                    result.append(menu_copy)
                else:
                    result.append(menu)

        return result

    def _check_menu_permission(self, menu: dict, user_permissions: set) -> bool:
        """
        检查用户是否有权限访问菜单

        Args:
            menu: 菜单信息
            user_permissions: 用户拥有的权限标识集合

        Returns:
            是否有权限
        """
        # 获取菜单对应的权限
        permission = self.repo.find(id=menu['id'])
        if not permission or not permission.perms:
            # 没有权限标识的菜单默认可见
            return True

        # 检查用户是否拥有该菜单的权限
        return permission.perms in user_permissions

    def _register_permission_resource(self, permission: Permission) -> None:
        """
        注册权限资源到Casbin

        Args:
            permission: 权限对象
        """
        if permission.perms:
            # 加载策略
            casbin_enforcer.e.load_policy()

            # 注册资源和资源角色的对应关系
            casbin_enforcer.e.add_named_policy("g2", permission.perms, permission.number)

    def _remove_permission_resource(self, permission: Permission) -> None:
        """
        从Casbin移除权限资源

        Args:
            permission: 权限对象
        """
        if permission.perms:
            # 加载策略
            casbin_enforcer.e.load_policy()

            # 移除资源和资源角色的对应关系
            casbin_enforcer.e.remove_named_policy("g2", permission.perms, permission.number)

    def _check_permission_in_use(self, permission: Permission) -> bool:
        """
        检查权限是否被角色使用

        Args:
            permission: 权限对象

        Returns:
            是否被使用
        """
        if permission.perms:
            # 加载策略
            casbin_enforcer.e.load_policy()

            # 检查是否有角色使用该权限
            policies = casbin_enforcer.e.get_policy()
            for policy in policies:
                if len(policy) >= 2 and policy[1] == permission.perms:
                    return True

        return False
