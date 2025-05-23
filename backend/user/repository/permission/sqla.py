

# sqla.py
import datetime as dt
from typing import Tuple, Type, List

from sqlalchemy import Column, DateTime, String, Table, Integer, Text, Boolean, event

from backend.extensions import db, mapper_registry
from backend.user.domain.permission import Permission
from backend.user.message import PERMISSION_EXISTS
from kit.exceptions import ServiceBadRequest
from kit.repository.sqla import SQLARepository

__all__ = ['PermissionSQLARepository']

from kit.util.sqla import id_column

permission = Table(
    'permission',
    mapper_registry.metadata,
    id_column(),
    Column('name', String(30), nullable=False, comment='权限名称'),
    Column('number', String(30), nullable=False, unique=True, comment='权限编号'),
    Column('parent_id', Integer, comment='父权限ID'),
    Column('level', Integer, nullable=False, comment='权限等级'),
    Column('path', String(255), comment='权限路径'),
    Column('component', String(255), comment='对应前端组件'),
    Column('icon', String(100), comment='图标'),
    Column('menu_type', Integer, default=0, comment='菜单类型(0:菜单,1:按钮)'),
    Column('perms', String(100), comment='权限标识'),
    Column('status', Integer, default=1, comment='状态(0:禁用,1:启用)'),
    Column('sort_order', Integer, default=0, comment='排序号'),
    Column('description', String(255), comment='权限描述'),
    Column('is_deleted', Integer, default=0, comment='是否删除(0:否,1:是)'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Permission, permission)


class PermissionSQLARepository(SQLARepository):
    """权限SQLAlchemy仓储实现"""

    @property
    def model(self) -> Type[Permission]:
        return Permission

    @property
    def query_params(self) -> Tuple:
        return ('parent_id', 'level', 'menu_type', 'status')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('name', 'number', 'perms')

    def get_permissions_by_level(self, level: int) -> List[Permission]:
        """
        获取指定等级的所有权限

        Args:
            level: 权限等级

        Returns:
            指定等级的权限列表
        """
        return self.session.query(Permission).filter(
            Permission.level == level,
            Permission.is_deleted == 0
        ).order_by(Permission.sort_order).all()

    def get_children(self, parent_id: int) -> List[Permission]:
        """
        获取指定权限的所有子权限

        Args:
            parent_id: 父权限ID

        Returns:
            子权限列表
        """
        return self.session.query(Permission).filter(
            Permission.parent_id == parent_id,
            Permission.is_deleted == 0
        ).order_by(Permission.sort_order).all()

    def build_permission_tree(self, parent_id: int = None) -> List[dict]:
        """
        构建权限树结构

        Args:
            parent_id: 父权限ID，默认为根权限

        Returns:
            权限树结构
        """
        # 如果parent_id是None，则获取所有顶级权限（parent_id为空的权限）
        if parent_id is None:
            permissions = self.session.query(Permission).filter(
                Permission.parent_id.is_(None),
                Permission.is_deleted == 0
            ).order_by(Permission.sort_order).all()
        else:
            permissions = self.get_children(parent_id)

        result = []
        for permission in permissions:
            # 递归获取子权限
            children = self.build_permission_tree(permission.id)
            # 构建当前权限节点
            permission_dict = {
                'id': permission.id,
                'name': permission.name,
                'path': permission.path,
                'perms': permission.perms,
                'children': children
            }
            result.append(permission_dict)

        return result

    def logical_delete(self, permission_id: int) -> None:
        """
        逻辑删除权限

        Args:
            permission_id: 权限ID
        """
        permission = self.get_by_id(permission_id)
        if permission:
            permission.is_deleted = 1
            self.session.commit()

