import datetime as dt
from typing import Tuple, Type

from sqlalchemy import BigInteger, Column, DateTime, String, Table, and_, event

from backend.extensions import mapper_registry, db
from backend.license_management.domain.li import License
from backend.user.domain import User, Department
from backend.user.message import UserMessage
from backend.user.repository.user.base import UserRepository
from kit.exceptions import ServiceBadRequest
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['UserSQLARepository']


user = Table(
    'user',
    mapper_registry.metadata,
    id_column(),
    Column('username', String(255), unique=True, comment='用户名'),
    Column('password', String(255), nullable=False, comment='密码'),
    Column('department_id', BigInteger, index=True, comment='部门ID'),
    Column('job_title', String(255), comment='职务'),
    Column('mobile', String(255), comment='电话'),
    Column('email', String(255), comment='邮箱'),
    Column('creator', String(255), comment='创建人'),
    Column('role_numbers', String(255), comment='角色编码'),
    Column('last_login_time', DateTime, comment='上次登录时间'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(User, user)


class UserSQLARepository(UserRepository, SQLARepository):
    def get_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def get_base_queryset(self):
        return (
            super()
            .get_base_queryset()
            .outerjoin(Department, Department.id == User.department_id)
            .add_entity(
                Department.name.label('department'),
            )
        )

    @property
    def model(self) -> Type[User]:
        return User

    @property
    def fuzzy_query_params(self) -> Tuple:
        return 'username', 'job_title'

    @property
    def in_query_params(self) -> Tuple:
        return 'department_id',

    def get_lis(self, unique_code: str):
        items = self.session.query(License.license).filter(
            and_(License.is_del == 0, License.unique_code == unique_code)).all()
        return [i[0] for i in items]

    def _get_conditions(self, **kwargs) -> list:
        conditions = list()
        if kwargs.get('role_number'):
            conditions.append(User.role_numbers.like(f'%{kwargs.pop("role_number")}%'))
        conditions.extend(super()._get_conditions(**kwargs))
        return conditions


@event.listens_for(User, 'before_insert')
def unique_user(mapper, connection, target: User):
    conditions = [User.username == target.username]
    if db.session.query(User).filter(*conditions).first():
        raise ServiceBadRequest(UserMessage.USER_EXISTED)


@event.listens_for(User, 'before_update')
def unique_user(mapper, connection, target: User):
    conditions = [User.username == target.username, User.id != target.id]
    if db.session.query(User).filter(*conditions).first():
        raise ServiceBadRequest(UserMessage.USER_EXISTED)
