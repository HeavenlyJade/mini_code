from typing import Type, Tuple,Dict,Any

from sqlalchemy import Column, String, Table, Integer, DateTime, Text
import datetime as dt

from backend.extensions import mapper_registry
from backend.mini_core.domain.specification import ShopSpecification, ShopSpecificationAttribute
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column, JsonText

__all__ = ['ShopSpecificationSQLARepository', 'ShopSpecificationAttributeSQLARepository']

# 商品规格表
shop_specification_table = Table(
    'shop_specification',
    mapper_registry.metadata,
    id_column(),
    Column('name', String(64), nullable=False, comment='规格名称'),
    Column('remark', Text, comment='备注'),
    Column('sort_order', Integer, comment='排序'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新者'),
)

# 商品规格属性表
shop_specification_attribute_table = Table(
    'shop_specification_attribute',
    mapper_registry.metadata,
    id_column(),
    Column('specification_id', Integer, nullable=False, comment='规格ID'),
    Column('name', String(64), nullable=False, comment='属性名称'),
    Column('attribute_value', JsonText, comment='属性内容'),
    Column('remark', Text, comment='备注'),
    Column('sort_order', Integer, comment='排序'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新者'),
)

# 映射
mapper_registry.map_imperatively(ShopSpecification, shop_specification_table)
mapper_registry.map_imperatively(ShopSpecificationAttribute, shop_specification_attribute_table)


class ShopSpecificationSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopSpecification]:
        return ShopSpecification

    @property
    def in_query_params(self) -> Tuple:
        return 'name',



class ShopSpecificationAttributeSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopSpecificationAttribute]:
        return ShopSpecificationAttribute

    @property
    def in_query_params(self) -> Tuple:
        return 'specification_id', 'name'

    def get_attributes_by_specification(self, specification_id: int):
        """获取指定规格ID的所有属性"""
        return self.find_all(specification_id=specification_id)

    def update_attribute(self, attribute_id: int, attribute: ShopSpecificationAttribute) -> Dict[str, Any]:
        # 获取现有实体
        entity = self.get_by_id(attribute_id)
        if not entity:
            return None

        # 直接在数据库实体上设置值
        entity.name = attribute.name
        entity.attribute_value = attribute.attribute_value  # 即使是空字典也会被设置
        entity.remark = attribute.remark
        entity.sort_order = attribute.sort_order
        entity.updater = attribute.updater
        # 保存更改
        self.session.commit()
        return dict(data=entity, code=200)
