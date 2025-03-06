import datetime as dt
from typing import Tuple, Type

from sqlalchemy import Column, DateTime, SmallInteger, String, Table, Text

from backend.extensions import mapper_registry
from backend.log.domain import Log
from backend.log.domain.log import LogOperatingType
from kit.repository.sqla import SQLARepository

__all__ = ['LogSQLARepository']

from kit.util.sqla import id_column

log = Table(
    'log',
    mapper_registry.metadata,
    id_column(),
    Column('operating_user', String(255), nullable=False, index=True, comment='操作用户'),
    Column('operating_type', SmallInteger, comment=LogOperatingType.desc()),
    Column('operating_detail', Text, comment='操作详情'),
    Column('operating_time', DateTime),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Log, log)


class LogSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[Log]:
        return Log

    @property
    def query_params(self) -> Tuple:
        return ('operating_type',)

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('operating_user',)

    @property
    def range_query_params(self) -> Tuple:
        return ('operating_time',)
