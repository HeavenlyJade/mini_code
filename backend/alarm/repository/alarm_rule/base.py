from abc import ABCMeta

from backend.alarm.domain import AlarmRule
from kit.repository.generic import GenericRepository

__all__ = ['AlarmRuleRepository']


class AlarmRuleRepository(GenericRepository[AlarmRule], metaclass=ABCMeta):
    ...
