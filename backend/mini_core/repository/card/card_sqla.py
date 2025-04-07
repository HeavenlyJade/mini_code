import datetime as dt
from typing import Type, Tuple

from flask_jwt_extended import get_current_user
from sqlalchemy import Column, String, Table, Integer, DateTime, or_, and_

from backend.extensions import mapper_registry
from backend.mini_core.domain.card import Card
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['CardSQLARepository']

card_table = Table(
    'card',
    mapper_registry.metadata,
    id_column(),
    Column('user_id', String(64), comment='用户编号'),
    Column('name', String(255), comment='用户名称'),
    Column('openid', Integer,  comment='微信ID'),
    Column('phone', String(255), comment='电话'),
    Column('weixing', String(255), comment='微信'),
    Column('position', String(255), comment='职位'),
    Column('company', String(255), comment='公司'),
    Column('creator', String(255), comment='创建人'),
    Column('image_url', String(255), comment='图片路由'),

    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Card, card_table)


class CardSQLARepository( SQLARepository):
    @property
    def model(self) -> Type[Card]:
        return Card

    @property
    def in_query_params(self) -> Tuple:
        return 'name','openid'





