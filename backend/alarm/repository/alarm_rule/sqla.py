import datetime as dt
from typing import Type

from sqlalchemy import Column, DateTime, Table, Float

from backend.alarm.domain import AlarmRule
from backend.extensions import mapper_registry
from kit.repository.sqla import SQLARepository

__all__ = ['AlarmRuleSQLARepository']

from kit.util.sqla import id_column

alarm = Table(
    'alarm_rule',
    mapper_registry.metadata,
    id_column(),
    Column('recipe_upper_limit', Float, comment='Recipe上限'),
    Column('recipe_lower_limit', Float, comment='Recipe下限'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(AlarmRule, alarm)


class AlarmRuleSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[AlarmRule]:
        return AlarmRule
