import datetime as dt
from typing import Tuple, Type, List

from sqlalchemy import Column, DateTime, String, Table, event

from backend.extensions import db, mapper_registry
from backend.role.domain import Role
from backend.role.domain.role import AccessLevel
from backend.role.message import ROLE_EXISTS
from kit.exceptions import ServiceBadRequest
from kit.repository.sqla import SQLARepository

__all__ = ['RoleSQLARepository']

from kit.util.sqla import id_column, JsonText

role = Table(
    'role',
    mapper_registry.metadata,
    id_column(),
    Column('role_number', String(255), index=True, comment='角色编码'),
    Column('access_level', String(255), comment=AccessLevel.desc()),
    Column('operation_terminal', String(255), comment='操作端'),
    Column('allowed_department_ids', JsonText),
    Column('areas', JsonText),
    Column('creator', String(255), comment='创建者'),
    Column('modifier', String(255), comment='修改者'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Role, role)


class CasbinRule(db.Model):
    __tablename__ = 'casbin_rule'

    id = id_column()
    ptype = db.Column(db.String(255))
    v0 = db.Column(db.String(255))
    v1 = db.Column(db.String(255))
    v2 = db.Column(db.String(255))
    v3 = db.Column(db.String(255))
    v4 = db.Column(db.String(255))
    v5 = db.Column(db.String(255))

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ', '.join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))


class RoleSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[Role]:
        return Role

    @property
    def fuzzy_query_params(self) -> Tuple:
        return (
            'role_number',
            'creator',
            'modifier',
        )

    def get_by_role_numbers(self, role_numbers: List[str]) -> List[Role]:
        return self.session.query(
            self.model
        ).filter(
            self.model.role_number.in_(role_numbers)
        ).all()


@event.listens_for(Role, 'before_insert')
def unique_role(mapper, connection, target: Role):
    conditions = [Role.role_number == target.role_number]
    if db.session.query(Role).filter(*conditions).first():
        raise ServiceBadRequest(ROLE_EXISTS)


@event.listens_for(Role, 'before_update')
def unique_role(mapper, connection, target: Role):
    conditions = [Role.role_number == target.role_number, Role.id != target.id]
    if db.session.query(Role).filter(*conditions).first():
        raise ServiceBadRequest(ROLE_EXISTS)
