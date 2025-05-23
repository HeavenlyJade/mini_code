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
    Column('permission_ids', JsonText),
    Column('areas', JsonText),
    Column('creator', String(255), comment='创建者'),
    Column('modifier', String(255), comment='修改者'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Role, role)


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

    def update_data(self, role_id: int, role_dict: dict):
        """
        更新角色数据

        Args:
            role_id: 角色ID
            role_dict: 要更新的角色数据字典

        Returns:
            更新后的角色对象，如果角色不存在则返回None
        """
        try:
            # 查询要更新的角色
            role = self.session.query(self.model).filter(
                self.model.id == role_id
            ).first()

            if not role:
                return None

            # 更新角色字段
            for key, value in role_dict.items():
                if hasattr(role, key):
                    setattr(role, key, value)

            # 设置更新时间
            if hasattr(role, 'update_time'):
                import datetime as dt
                role.update_time = dt.datetime.now()

            # 提交更改
            self.session.commit()

            return role

        except Exception as e:
            # 发生错误时回滚事务
            self.session.rollback()
            raise e


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
