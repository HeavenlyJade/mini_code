from abc import ABCMeta

from backend.alarm.domain import Alarm
from kit.repository.generic import GenericRepository

__all__ = ['AlarmRepository']


class AlarmRepository(GenericRepository[Alarm], metaclass=ABCMeta):
    ...
