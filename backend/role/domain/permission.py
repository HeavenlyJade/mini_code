from dataclasses import field
from typing import Optional, List
from datetime import datetime
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity
from kit.domain.field import ExtendedEnum
from kit.domain.types import StrField

__all__ = ['Permission', 'MenuType', 'PermissionStatus']


class MenuType(ExtendedEnum):
    """菜单类型枚举"""

    DIRECTORY = 0
    MENU = 1
    BUTTON = 2

    @classmethod
    def comparison_map(cls) -> dict:
        return {
            0: '目录',
            1: '菜单',
            2: '按钮'
        }


class PermissionStatus(ExtendedEnum):
    """权限状态枚举"""

    DISABLED = 0
    ENABLED = 1

    @classmethod
    def comparison_map(cls) -> dict:
        return {
            0: '禁用',
            1: '启用'
        }


@dataclass
class Permission(Entity):
    """
    权限领域模型

    用于表示系统权限信息，包括菜单、按钮等各种权限节点
    """
    name: StrField = field(
        metadata=dict(required=True, description='权限名称'),
        default=None
    )

    number: StrField = field(
        metadata=dict(required=True, description='权限编号'),
        default=None
    )

    parent_id: Optional[int] = field(
        metadata=dict(description='父权限ID'),
        default=None
    )

    level: int = field(
        metadata=dict(description='权限等级'),
        default=1
    )

    path: Optional[StrField] = field(
        metadata=dict(description='权限路径'),
        default=None
    )

    component: Optional[StrField] = field(
        metadata=dict(description='对应前端组件'),
        default=None
    )

    icon: Optional[StrField] = field(
        metadata=dict(description='图标'),
        default=None
    )

    menu_type: MenuType = field(
        metadata=dict(
            description=MenuType.desc(),
            by_value=True,
        ),
        default=MenuType.MENU
    )

    perms: Optional[StrField] = field(
        metadata=dict(description='权限标识'),
        default=None
    )

    status: PermissionStatus = field(
        metadata=dict(
            description=PermissionStatus.desc(),
            by_value=True,
        ),
        default=PermissionStatus.ENABLED
    )

    sort_order: int = field(
        metadata=dict(description='排序号'),
        default=0
    )

    description: Optional[StrField] = field(
        metadata=dict(description='权限描述'),
        default=None
    )

    is_deleted: bool = field(
        metadata=dict(description='是否删除(0:否,1:是)'),
        default=False
    )

    # 权限树相关的辅助属性（不存储到数据库）
    children: List['Permission'] = field(
        default_factory=list,
        metadata=dict(dump_only=True, description='子权限列表')
    )

    def get_menu_type_display(self) -> str:
        """获取菜单类型显示名称"""
        return MenuType.get_display_name(self.menu_type)

    def get_status_display(self) -> str:
        """获取状态显示名称"""
        return PermissionStatus.get_display_name(self.status)

    def is_directory(self) -> bool:
        """判断是否为目录"""
        return self.menu_type == MenuType.DIRECTORY

    def is_menu(self) -> bool:
        """判断是否为菜单"""
        return self.menu_type == MenuType.MENU

    def is_button(self) -> bool:
        """判断是否为按钮"""
        return self.menu_type == MenuType.BUTTON

    def is_enabled(self) -> bool:
        """判断是否启用"""
        return self.status == PermissionStatus.ENABLED

    def has_children(self) -> bool:
        """判断是否有子权限"""
        return len(self.children) > 0

    def add_child(self, child: 'Permission') -> None:
        """添加子权限"""
        if child not in self.children:
            self.children.append(child)
            child.parent_id = self.id
            child.level = self.level + 1

    def remove_child(self, child: 'Permission') -> None:
        """移除子权限"""
        if child in self.children:
            self.children.remove(child)
            child.parent_id = None

    def get_full_path(self) -> str:
        """获取完整路径（包含父级路径）"""
        if self.parent_id is None:
            return self.path or ''
        # 这里需要根据实际需求实现父级路径查找逻辑
        return self.path or ''

    def to_tree_node(self) -> dict:
        """转换为树形节点格式（用于前端展示）"""
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'parent_id': self.parent_id,
            'level': self.level,
            'path': self.path,
            'component': self.component,
            'icon': self.icon,
            'menu_type': self.menu_type.value if isinstance(self.menu_type, MenuType) else self.menu_type,
            'menu_type_display': self.get_menu_type_display(),
            'perms': self.perms,
            'status': self.status.value if isinstance(self.status, PermissionStatus) else self.status,
            'status_display': self.get_status_display(),
            'sort_order': self.sort_order,
            'description': self.description,
            'children': [child.to_tree_node() for child in self.children],
            'create_time': self.create_time,
            'update_time': self.update_time
        }


@dataclass
class RolePermission(Entity):
    """
    角色权限关联领域模型

    用于表示角色和权限的多对多关系
    """
    role_id: int = field(
        metadata=dict(required=True, description='角色ID'),
        default=None
    )

    permission_id: int = field(
        metadata=dict(required=True, description='权限ID'),
        default=None
    )

    # 关联对象（不存储到数据库）
    role: Optional['Role'] = field(
        default=None,
        metadata=dict(dump_only=True, description='关联的角色对象')
    )

    permission: Optional[Permission] = field(
        default=None,
        metadata=dict(dump_only=True, description='关联的权限对象')
    )
