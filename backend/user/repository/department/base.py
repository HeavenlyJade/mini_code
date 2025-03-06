from abc import ABCMeta, abstractmethod

from backend.user.domain import Department
from kit.repository.generic import GenericRepository

__all__ = ['DepartmentRepository']


class DepartmentRepository(GenericRepository[Department], metaclass=ABCMeta):
    ...
