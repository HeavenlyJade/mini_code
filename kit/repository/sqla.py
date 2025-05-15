from abc import abstractmethod
from dataclasses import asdict
from typing import Any, Dict, List, NoReturn, Optional, Sequence, Tuple, Type,Union
from flask import g
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from kit.domain.entity import Entity,EntityInt
from kit.exceptions import ServiceBadRequest
from kit.message import GlobalMessage
from kit.repository.generic import GenericRepository

__all__ = ['SQLARepository']


class SQLARepository(GenericRepository[Entity]):
    def __init__(self, session: Session):
        self.session: Session = session

    @property
    @abstractmethod
    def model(self) -> Type[Entity]:
        ...

    @property
    def query_params(self) -> Tuple:
        return tuple()

    @property
    def fuzzy_query_params(self) -> Tuple:
        return tuple()

    @property
    def in_query_params(self) -> Tuple:
        return tuple()

    @property
    def range_query_params(self) -> Tuple:
        return tuple()

    def get_fields_by_names(self, field_names: List[str] = None) -> List[dict]:
        """
        根据传入的字段名列表，返回对应的数据库查询结果字典列表

        Args:
            field_names: 要查询的字段名列表，如果为None则返回所有字段

        Returns:
            包含查询结果的字典列表
        """
        # 如果没有传入字段，则使用所有字段
        if not field_names or len(field_names) == 0:
            # 获取所有查询结果并转为字典
            query_result = self.session.query(self.model).all()
            return [asdict(item) for item in query_result]

        # 构建有效字段列表
        valid_fields = []
        valid_field_names = []
        for field_name in field_names:
            if hasattr(self.model, field_name):
                valid_fields.append(getattr(self.model, field_name))
                valid_field_names.append(field_name)

        # 如果没有有效字段，返回空列表
        if not valid_fields:
            return []

        # 执行查询
        queryset = self.session.query(*valid_fields)
        results = queryset.all()

        # 将结果转换为字典列表
        result_dicts = []
        for row in results:
            # 如果只查询了一个字段，row可能不是元组
            if len(valid_field_names) == 1:
                row_dict = {valid_field_names[0]: row}
            else:
                # 将查询结果和字段名对应起来创建字典
                row_dict = {field_name: value for field_name, value in zip(valid_field_names, row)}
            result_dicts.append(row_dict)

        return result_dicts

    def list(self, **kwargs) -> Tuple[List[Entity], int]:
        query = self.get_queryset(**kwargs)
        total = query.count() if kwargs.get('need_total_count') else 0

        if kwargs.get('page') and kwargs.get('size'):
            query = self.and_pagination(query, kwargs['page'], kwargs['size'])

        return query.all(), total
    @property
    def get_base_queryset(self):
        queryset = self.session.query(self.model)
        return queryset

    def get_queryset(self, **kwargs):
        conditions = self._get_conditions(**kwargs)
        sort_conditions = self._get_sort_conditions(**kwargs)
        return self.session.query(self.model).filter(*conditions).order_by(*sort_conditions)

    def get_all(self, **kwargs) -> List[Entity]:
        query = self.get_queryset(**kwargs)
        return query.all()

    def get_by_id(self, entity_id: int) -> Optional[Entity]:
        if entity_id is None:
            return None
        return self.session.get(self.model, entity_id)

    def create(self, entity: Entity, commit: bool = True, flush: bool = False) -> Entity:
        if isinstance(entity, dict):
            entity = self.model(**entity)
        if hasattr(entity, 'creator') and hasattr(g, 'creator'):
            setattr(entity, 'creator', g.creator)
        if hasattr(entity, 'create_department_id') and hasattr(g, 'create_department_id'):
            setattr(entity, 'create_department_id', g.create_department_id)
        self.session.add(entity)
        if commit:
            self.session.commit()
        if flush:
            self.session.flush()
        return entity

    def create_many(self, entities: List[Entity], commit: bool = True) -> NoReturn:
        self.session.add_all(entities)
        if commit:
            self.session.commit()

    def update(
        self,
        entity_id: int,
        entity: Entity,
        commit: bool = True,
        ignore_null=True,
    ) -> Optional[Entity]:
        e = self.session.query(self.model).with_for_update().get(entity_id)
        if not e:
            return e

        if ignore_null:
            properties = asdict(
                entity, dict_factory=lambda x: {k: v for (k, v) in x if v or v == 0}
            )
        else:
            properties = asdict(entity)
        for key, value in properties.items():
            setattr(e, key, value)
        if commit:
            self.session.commit()
        return e

    def delete(self, entity_id: int,commit: bool = True):
        self.session.query(self.model).filter_by(id=entity_id).delete()
        # self.session.commit()
        if commit:
            self.session.commit()

    def batch_delete(self, ids: List[int], commit: bool = True):
        """
        批量删除指定ID的实体

        :param ids: 要删除的实体ID列表
        :param commit: 是否立即提交事务，默认为True
        :return: 删除的记录数
        """
        if not ids:
            raise ServiceBadRequest("未提供要删除的ID列表")

        deleted_count = self.session.query(self.model).filter(
            self.model.id.in_(ids)
        ).delete(synchronize_session=False)

        if commit:
            self.session.commit()

        return deleted_count
    def delete_by(self, conditions: Dict[str, Any], commit: bool = True):
        conditions = [
            getattr(self.model, field) == value for field, value in conditions.items()
        ]
        if not conditions:
            raise ServiceBadRequest(GlobalMessage.DELETE_NO_CONDITIONS)

        self.session.query(self.model).filter(*conditions).delete(
            synchronize_session=False
        )
        if commit:
            self.session.commit()

    def find(self, row_locked: bool = False, **kwargs) :
        query = self.session.query(self.model).filter_by(**kwargs)
        if row_locked:
            query = query.with_for_update()
        return query.first()

    def find_by_ids(self, ids: Sequence[int]) -> List[Entity]:
        query = self.session.query(self.model).filter(self.model.id.in_(ids))
        return query.all()

    def find_all(self, **kwargs) -> List[Entity]:
        print("1321",kwargs,self.model)
        query = self.session.query(self.model).filter_by(**kwargs)
        return query.all()

    def flush(self) -> None:
        self.session.flush()

    def _get_conditions(self, **kwargs) -> list:
        if hasattr(g, 'allowed_department_ids'):
            kwargs['allowed_department_ids'] = g.allowed_department_ids
        if hasattr(g, 'creator'):
            kwargs['creator'] = g.creator
        conditions = list()
        for param, value in kwargs.items():
            # FIXME: Since data permissions are required for all data,
            # querying is probably the easiest solution here.
            # But it also means that you need to implement similar
            # permission pre-checking in each specific repository implementation.
            # if param == 'allowed_department_ids' and hasattr(self.model, 'create_department_id'):
            #     conditions.append(or_(
            #         getattr(self.model, 'create_department_id').in_(value),
            #         getattr(self.model, 'create_department_id').is_(None),
            #     ))
            # elif param == 'creator' and hasattr(self.model, 'creator'):
            #     conditions.append(or_(
            #         getattr(self.model, 'creator') == value,
            #         getattr(self.model, 'creator').is_(None),
            #     ))

            if param in self.query_params:
                conditions.append(getattr(self.model, param) == value)
            elif param in self.fuzzy_query_params:
                conditions.append(getattr(self.model, param).like(f'%{value}%'))
            elif param in self.in_query_params:
                conditions.append(getattr(self.model, param).in_(value))
            elif param in self.range_query_params:
                start, end = value
                if start:
                    conditions.append(getattr(self.model, param) >= start)
                if end:
                    conditions.append(getattr(self.model, param) <= end)
        return conditions

    def _get_sort_conditions(self, **kwargs) -> List:
        sort_conditions = list()
        if kwargs.get('ordering'):
            ordering = kwargs['ordering']
            self._update_ordering(self.model, ordering, sort_conditions)
        return sort_conditions

    @classmethod
    def and_pagination(cls, query, page: int = 1, size: int = 10):
        pos = (page - 1) * size
        return query.limit(size).offset(pos)

    @classmethod
    def _update_ordering(
        cls, model_class: Type[Entity], ordering: List[str], sort_conditions: list
    ):
        for field in ordering:
            is_reverse = False
            if field.startswith('-'):
                field = field[1:]
                is_reverse = True

            if not hasattr(model_class, field):
                continue
            sort_condition = (
                desc(getattr(model_class, field))
                if is_reverse
                else asc(getattr(model_class, field))
            )
            sort_conditions.append(sort_condition)

    def commit(self) -> None:
        self.session.commit()
