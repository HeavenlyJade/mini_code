import datetime as dt
from typing import Type, Tuple

from flask_jwt_extended import get_current_user
from sqlalchemy import Column, String, Table, Integer, DateTime, or_, and_

from backend.extensions import mapper_registry
from backend.user.domain import User, Department
from backend.user.repository.department.base import DepartmentRepository
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['DepartmentSQLARepository']

department = Table(
    'department',
    mapper_registry.metadata,
    id_column(),
    Column('name', String(255), unique=True, comment='部门名称'),
    Column('level', Integer, nullable=False, comment='部门层级'),
    Column('parent_id', Integer, comment='上级部门id'),
    Column('creator', String(255), comment='创建人'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Department, department)


class DepartmentSQLARepository(DepartmentRepository, SQLARepository):
    @property
    def model(self) -> Type[Department]:
        return Department

    @property
    def in_query_params(self) -> Tuple:
        return 'parent_id',

    def _get_conditions(self, **kwargs) -> list:
        # The Creator can see the departments he created.
        conditions = super()._get_conditions(**kwargs)
        if not conditions:
            return conditions

        user = get_current_user()
        return [or_(and_(*conditions), Department.creator == user.username)]



