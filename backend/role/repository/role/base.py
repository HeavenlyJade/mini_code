from abc import ABCMeta

from backend.role.domain import Role
from kit.repository.generic import GenericRepository

__all__ = ['RoleRepository']


class RoleRepository(GenericRepository[Role], metaclass=ABCMeta):
    ...
