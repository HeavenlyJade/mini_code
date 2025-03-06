from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Sequence, Tuple, TypeVar

from kit.domain.entity import Entity

__all__ = ['GenericRepository']

T = TypeVar('T', bound=Entity)


class GenericRepository(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def list(self, **kwargs) -> Tuple[List[T], int]:
        """Returns entity instances and the count of entities."""

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Return an entity based on the given primary key identifier, or ``None`` if not found."""

    @abstractmethod
    def create(self, entity: T, commit: bool = True, flush: bool = False) -> T:
        ...

    @abstractmethod
    def update(self, entity_id: int, entity: T, commit: bool = True) -> Optional[T]:
        """Update and return an entity based on the given primary key identifier, or ``None`` if not found."""

    @abstractmethod
    def delete(self):
        ...

    @abstractmethod
    def delete_by(self, conditions: Dict[str, Any], commit: bool = True):
        """批量条件删除

        Notes: 传入条件不能为空

        """
        ...

    @abstractmethod
    def create_many(self, entities: List[T], commit: bool = True) -> None:
        ...

    @abstractmethod
    def find(self, **kwargs) -> Optional[T]:
        """Find an entity based on the given conditions, or ``None`` if not found."""

    @abstractmethod
    def find_by_ids(self, ids: Sequence[int]) -> List[T]:
        """Find all entities based on the given ids."""

    @abstractmethod
    def find_all(self, **kwargs) -> List[T]:
        """Find all entities based on the given conditions."""

    @abstractmethod
    def get_all(self, **kwargs) -> List[T]:
        ...

    @abstractmethod
    def commit(self) -> None:
        ...
