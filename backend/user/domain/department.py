from dataclasses import dataclass, field
from typing import Optional, List

from kit.domain.entity import Entity


__all__ = ['Department']


@dataclass
class Department(Entity):
    name: str = field(
        metadata=dict(
            required=True,
            description='部门名称'
        )
    )
    level: Optional[int] = field(
        metadata=dict(
            description='部门层级',
            dump_only=True,
        ),
        default=0,
    )
    parent_id: Optional[int] = field(
        metadata=dict(
            required=True,
            description='上级部门id'
        ),
        default=None,
    )
    creator: str = field(init=False)
