from abc import ABCMeta
from typing import Generic, List, Optional, TypeVar

from flask import abort, g

from kit.domain.entity import Entity
from kit.repository.generic import GenericRepository

__all__ = ['CRUDService']

T = TypeVar('T', bound=Entity)


class CRUDService(Generic[T], metaclass=ABCMeta):
    def __init__(self, repo: GenericRepository[T]):
        self._repo = repo

    @property
    def repo(self) -> GenericRepository[T]:
        return self._repo

    def list(self, args: dict) -> dict:
        if hasattr(g, 'allowed_department_ids'):
            args['allowed_department_ids'] = g.allowed_department_ids
        if hasattr(g, 'creator'):
            args['creator'] = g.creator
        items, total = self.repo.list(**args)
        return dict(items=items, total=total)

    def get(self, entity_id: int) -> Optional[T]:
        """Return an entity based on the given primary key identifier, or ``abort 404`` if not found."""
        entity = self.repo.get_by_id(entity_id)
        if not entity:
            abort(404)
        return entity

    def create(self, entity: T) -> T:
        if hasattr(entity, 'creator') and hasattr(g, 'creator'):
            setattr(entity, 'creator', g.creator)
        return self.repo.create(entity)

    def create_many(self, entities: List[Entity]) -> None:
        self.repo.create_many(entities)

    def update(self, entity_id: int, entity: Entity) -> Optional[T]:
        """Update and return an entity based on the given primary key identifier, or ``abort 404`` if not found."""
        entity = self.repo.update(entity_id, entity)
        if not entity:
            abort(404)
        return entity

    def delete(self, entity_id: int) -> None:
        self.repo.delete(entity_id)
