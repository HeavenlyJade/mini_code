from typing import Type, Tuple

from sqlalchemy import Column, String, Table, Integer, DateTime, Text, Enum, Boolean
import datetime as dt

from backend.extensions import mapper_registry
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column
from backend.mini_core.domain.store import ShopStoreCategory

__all__ = ['ShopStoreCategorySQLARepository']

# 商店分类表
shop_store_category_table = Table(
    'shop_store_category',
    mapper_registry.metadata,
    id_column(),
    Column('name', String(64), nullable=False, comment='分类名称'),
    Column('code', String(32), comment='分类编码'),
    Column('parent_id', Integer, comment='上级分类ID'),
    Column('icon', String(255), comment='图标路径'),
    Column('image', String(255), comment='图片路径'),
    Column('sort_order', Integer, comment='排序'),
    Column('status', Enum('正常', '停用'), comment='状态'),
    Column('remark', Text, comment='备注说明'),
    Column('is_recommend', Boolean, default=False, comment='是否推荐'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

# 映射
mapper_registry.map_imperatively(ShopStoreCategory, shop_store_category_table)


class ShopStoreCategorySQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopStoreCategory]:
        return ShopStoreCategory

    @property
    def in_query_params(self) -> Tuple:
        return 'name', 'code', 'parent_id', 'status'

    def get_category_tree(self):
        """
        获取所有分类的树状结构

        返回：
            所有分类的树状结构
        """
        # 先获取所有分类
        all_categories = self.find()

        # 构建树结构
        def build_tree(parent_id=None):
            children = [c for c in all_categories if c.parent_id == parent_id]
            result = []
            for child in children:
                node = {
                    'id': child.id,
                    'name': child.name,
                    'code': child.code,
                    'sort_order': child.sort_order,
                    'status': child.status,
                    'is_recommend': child.is_recommend,
                    'children': build_tree(child.id)
                }
                result.append(node)
            return result

        return build_tree()
