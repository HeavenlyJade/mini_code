# -*- coding: utf-8 -*-
# author zyy
import datetime as dt
from typing import Type

from sqlalchemy import (
    Column,
    DateTime,
    SmallInteger,
    String,
    Table,
    and_,
)

from backend.extensions import mapper_registry
from backend.license_management.domain.li import License
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['LiSQLARepository']

license_manage = Table(
    'license_management',
    mapper_registry.metadata,
    id_column(),
    Column(
        'customer_name', String(50), nullable=False, unique=True, comment='客户名称'
    ),
    Column(
        'unique_code', String(50), nullable=False, comment='设备唯一识别码'
    ),
    Column(
        'license', String(2000), nullable=False, comment='license'
    ),
    Column(
        'start_time', DateTime, comment='有效期开始时间'
    ),
    Column(
        'end_time', DateTime,  comment='有效期开始时间'
    ),
    Column(
        'is_del', SmallInteger, nullable=False, comment='是否删除'
    ),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(License, license_manage)


class LiSQLARepository(SQLARepository):

    @property
    def model(self) -> Type[License]:
        return License

    def find_time(self, args):
        if args['start_time'] or args['end_time']:
            if not args['end_time']:
                args['end_time'] = args['start_time']
            if not args['start_time']:
                args['start_time'] = args['end_time']
            items = self.session.query(self.model).filter(
                and_(self.model.start_time > args['start_time'], self.model.is_del == 0 ,self.model.end_time < args['end_time'])).limit(
                int(args['size'])).offset((int(args['page']) - 1) * int(args['size'])).all()
            count = self.session.query(self.model).filter(
                and_(self.model.start_time > args['start_time'], self.model.is_del == 0, self.model.end_time < args['end_time'])).count()
            return {'items': items, 'total': count}
        items = self.session.query(self.model).filter(self.model.is_del == 0 ).limit(int(args['size'])).offset((int(args['page']) - 1) * int(args['size'])).all()
        count = self.session.query(self.model).filter(self.model.is_del == 0 ).count()
        return {'items': items, 'total': count}

    def delete_li(self, id):
        res = self.session.query(self.model).filter_by(id = id).update({self.model.is_del: 1})
        if res:
            self.session.commit()
        return res

    def is_exist(self,  license)->bool:
        items = self.session.query(self.model).filter(and_(self.model.is_del == 0, self.model.license == license)).all()
        if items:
            return True
        return False



