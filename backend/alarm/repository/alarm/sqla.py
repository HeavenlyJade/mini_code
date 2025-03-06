import datetime as dt
from typing import Tuple, Type

from sqlalchemy import BigInteger, Column, DateTime, String, Table, Text

from backend.alarm.domain.alarm import Alarm
from backend.extensions import mapper_registry
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['AlarmSQLARepository']

alarm = Table(
    'alarm',
    mapper_registry.metadata,
    id_column(),
    Column('message', Text, comment='报警信息'),
    Column('alarm_time', DateTime, index=True, default=dt.datetime.now),
    Column('task_id', String(255), index=True),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Alarm, alarm)


class AlarmSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[Alarm]:
        return Alarm

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('eqp_name',)

    @property
    def range_query_params(self) -> Tuple:
        return ('alarm_time',)
