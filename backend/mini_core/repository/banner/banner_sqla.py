# backend/business/repository/banner/sqla.py
import datetime as dt
from typing import Tuple, Type

from sqlalchemy import Column, DateTime, String, Table, Integer, Text, event

from backend.extensions import mapper_registry
from backend.mini_core.domain.banner import Banner
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['BannerSQLARepository']

banner = Table(
    'banner',
    mapper_registry.metadata,
    id_column(),
    Column('code_type', String(50), nullable=False, comment='自定义类型'),
    Column('business_code', String(50), default='0', comment='业务编号'),
    Column('name', String(100), nullable=False, comment='横幅名称'),
    Column('upload_image', String(255), comment='上传图片路径'),
    Column('upload_video', String(500), comment='上传视频路径'),
    Column('expand_image', String(255), comment='扩展图片路径'),
    Column('link_type', String(20), comment='链接类型'),
    Column('link_url', String(255), comment='链接地址'),
    Column('remark', Text, comment='备注'),
    Column('status', Integer, default=1, comment='状态(1-显示,0-隐藏)'),
    Column('sort_order', Integer, default=10, comment='排序'),
    Column('creator', String(64), comment='创建人'),
    Column('updater', String(64), comment='更新人'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

mapper_registry.map_imperatively(Banner, banner)


class BannerSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[Banner]:
        return Banner

    @property
    def query_params(self) -> Tuple:
        return ('code_type', 'business_code', 'status')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('name',)
