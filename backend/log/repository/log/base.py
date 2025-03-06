from abc import ABCMeta

from backend.log.domain import Log
from kit.repository.generic import GenericRepository

__all__ = ['LogRepository']


class LogRepository(GenericRepository[Log], metaclass=ABCMeta):
    ...
