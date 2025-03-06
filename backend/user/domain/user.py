from dataclasses import field
from typing import List, Optional

from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity
from kit.domain.types import DateTimeField, StrField

__all__ = ['User']


@dataclass
class Permission:
    obj: str = field(
        metadata=dict(
            required=True,
            description='访问资源',
        )
    )
    act: str = field(
        metadata=dict(
            required=True,
            description='访问方法',
        )
    )


@dataclass
class User(Entity):
    username: StrField = field(
        default=None,
        metadata=dict(
            required=True,
            description='用户名',
        ),
    )
    password: StrField = field(
        default=None,
        metadata=dict(
            load_only=True,
            description='密码',
        ),
    )
    department_id: int = field(default=None, metadata=dict(description='部门ID'))
    department: StrField = field(default=None, metadata=dict(description='部门'))
    job_title: StrField = field(default=None, metadata=dict(description='职务'))
    mobile: StrField = field(default=None, metadata=dict(description='电话'))
    email: StrField = field(default=None, metadata=dict(description='邮箱'))
    creator: StrField = field(
        default=None, metadata=dict(dump_only=True, description='创建人')
    )
    last_login_time: DateTimeField = field(
        default=None, metadata=dict(dump_only=True, description='上次登录时间')
    )

    role_numbers: str = field(default=None, metadata=dict(description='角色编码列表'))
    permissions: List[Permission] = field(
        default=None, metadata=dict(dump_only=True, description='权限列表')
    )
    areas: Optional[List[str]] = field(
        default=None,
        metadata=dict(description='区域列表', dump_only=True),
    )
    allowed_department_ids: List[int] = field(
        default_factory=list,
        metadata=dict(
            dump_only=True,
        )
    )
