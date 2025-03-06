from abc import ABCMeta, abstractmethod

from backend.user.domain import User
from kit.repository.generic import GenericRepository

__all__ = ['UserRepository']


class UserRepository(GenericRepository[User], metaclass=ABCMeta):
    @abstractmethod
    def get_by_username(self, username: str):
        ...
