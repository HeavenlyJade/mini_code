from dataclasses import dataclass, field
from typing import List, Optional

from kit.domain.entity import Entity
from kit.domain.types import StrField


@dataclass
class Permission(Entity):
    """权限领域模型"""

    name: StrField = field(
        default=None,
        metadata=dict(
            required=True,
            description='权限名称',
        ),
    )
    number: StrField = field(
        default=None,
        metadata=dict(
            required=True,
            description='权限编号',
        ),
    )
    parent_id: Optional[int] = field(
        default=None,
        metadata=dict(
            description='父权限ID',
        ),
    )
    level: int = field(
        default=None,
        metadata=dict(
            required=True,
            description='权限等级',
        ),
    )
    path: StrField = field(
        default=None,
        metadata=dict(
            description='权限路径',
        ),
    )
    component: StrField = field(
        default=None,
        metadata=dict(
            description='对应前端组件',
        ),
    )
    icon: StrField = field(
        default=None,
        metadata=dict(
            description='图标',
        ),
    )
    menu_type: int = field(
        default=0,
        metadata=dict(
            description='菜单类型(0:菜单,1:按钮)',
        ),
    )
    perms: StrField = field(
        default=None,
        metadata=dict(
            description='权限标识',
        ),
    )
    status: int = field(
        default=1,
        metadata=dict(
            description='状态(0:禁用,1:启用)',
        ),
    )
    sort_order: int = field(
        default=0,
        metadata=dict(
            description='排序号',
        ),
    )
    description: StrField = field(
        default=None,
        metadata=dict(
            description='权限描述',
        ),
    )
    is_deleted: int = field(
        default=0,
        metadata=dict(
            description='是否删除(0:否,1:是)',
        ),
    )
