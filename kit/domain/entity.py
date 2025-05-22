import datetime as dt
import uuid
from dataclasses import dataclass, field

__all__ = ['Entity', 'EntityInt','SoftDeleteMixin', 'UuidEntity', 'DataPermissionMixin']

from typing import Optional


@dataclass
class Entity:
    id: int = field(init=False,metadata=dict(dump_only=True,),)
    create_time: dt.datetime = field(
        init=False,
        metadata=dict(
            dump_only=True,
        ),
    )
    update_time: dt.datetime = field(
        init=False,
        metadata=dict(
            dump_only=True,
        ),
    )

@dataclass
class EntityInt(Entity):
    id: int = field(init=False,metadata=dict(dump_only=True,),)
    create_time: dt.datetime = field(default=None, metadata=dict(description='创建时间'))
    update_time: dt.datetime = field(default=None, metadata=dict(description='更新时间'))
    delete_time: dt.datetime = field(default=None, metadata=dict(description='删除时间'))


@dataclass
class UuidEntity(Entity):
    id: str = field(hash=True, init=False)


@dataclass
class SoftDeleteMixin:
    delete_time: int = field(
        init=False,
        metadata=dict(
            load_only=True,
            dump_only=True,
        ),
    )


@dataclass
class DataPermissionMixin:
    create_department_id: Optional[int] = field(
        init=False,
        metadata=dict(
            load_only=True,
            dump_only=True,
        )
    )
    creator: Optional[str] = field(
        init=False,
        metadata=dict(
            load_only=True,
            dump_only=True,
        )
    )
