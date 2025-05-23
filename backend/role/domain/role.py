from dataclasses import dataclass, field
from typing import List, Union, Optional

from kit.domain.entity import Entity
from kit.domain.field import ExtendedEnum
from kit.domain.types import StrField

__all__ = ['Role', 'AccessLevel']


class AccessLevel(ExtendedEnum):
    """数据查看范围等级"""

    ALL_DEPT = 'all_dept'
    TARGET_DEPT = 'target_dept'
    OWN_DEPT = 'own_dept'
    OWN_SUB_DEPT = 'own_sub_dept'
    ONESELF = 'oneself'

    @classmethod
    def comparison_map(cls) -> dict:
        return {
            'all_dept': '所有部门',
            'target_dept': '指定部门',
            'own_dept': '本部门',
            'own_sub_dept': '本部门以及所有下级部门',
            'oneself': '本人',
        }


class OperationTerminal(ExtendedEnum):
    """操作端"""

    It = 'IT'
    USER = 'User'
    IT_AND_USER = 'IT_and_User'

    @classmethod
    def comparison_map(cls) -> dict:
        return {
            'IT': 'IT端',
            'User': 'User端',
            'IT_and_User': 'IT端&User端',
        }


@dataclass
class Role(Entity):
    role_number: StrField = field(
        metadata=dict(required=True, description='角色编码')
    )
    access_level: Optional[Union[AccessLevel, str]] = field(
        metadata=dict(
            description=AccessLevel.desc(),
            by_value=True,
        ),
        default=None,
    )
    permission_ids:List[int] = field(
        default_factory=list,
    )
    allowed_department_ids: List[int] = field(
        metadata=dict(
            description='允许访问的部门ID列表',
            by_value=True,
            allow_none=True,
        ),
        default_factory=list,
    )
    areas: Optional[List[str]] = field(
        default_factory=list,
    )
    creator: StrField = field(
        default=None,
        metadata=dict(
            required=True,
            description='创建者',
        ),
    )
    modifier: StrField = field(
        default=None,
        metadata=dict(
            required=True,
            description='修改者',
        ),
    )
    operation_terminal: Optional[Union[OperationTerminal, str]] = field(
        metadata=dict(
            description=OperationTerminal.desc(),
            by_value=True,
        ),
        default=None,
    )

    def get_allowed_department_ids(self) -> list:
        if self.access_level == AccessLevel.TARGET_DEPT.value:
            return self.allowed_department_ids
        return []
