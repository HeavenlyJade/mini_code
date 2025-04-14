import datetime as dt
from typing import Type, Tuple

from flask_jwt_extended import get_current_user
from sqlalchemy import Column, String, Table, Integer, DateTime, Text, Enum, Boolean, Numeric, ForeignKey,JSON
from kit.util.sqla import id_column, JsonText
from backend.extensions import mapper_registry
from backend.mini_core.domain.shop import ShopProductCategory, ShopProduct
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['ShopProductCategorySQLARepository', 'ShopProductSQLARepository']

product_category_table = Table(
    'shop_product_category',
    mapper_registry.metadata,
    id_column(),
    Column('name', String(64), nullable=False, comment='分类名称'),
    Column('remark', Text, comment='备注'),
    Column('type', String(32), comment='类型'),
    Column('parent_id', Integer, comment='上级分类ID'),
    Column('code', String(32), comment='编号'),
    Column('icon', Text, comment='图标路径'),
    Column('image', Text, comment='图片路径'),
    Column('sort_order', Integer, comment='排序'),
    Column('status', Enum('正常', '停用'), comment='状态'),
    Column('is_audit', Boolean, default=False, comment='是否审核'),
    Column('audit_type', Enum('自动', '人工'), comment='审核类型'),
    Column('store_id', Integer, comment='所属门店ID'),
    Column('attribute', JSON, comment='attribute'),
    Column('content', Text, comment='内容'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

shop_product_table = Table(
    'shop_product',
    mapper_registry.metadata,
    id_column(),
    Column('category_id', Integer, comment='商品分类ID'),
    Column('code', String(32), comment='商品编号'),
    Column('name', String(128), nullable=False, comment='商品名称'),
    Column('alias', String(64), comment='别名'),
    Column('type', Enum('实物商品', '虚拟商品'), comment='类型'),
    Column('support_overseas_shipping', Boolean, default=False, comment='是否支持海外直邮'),
    Column('keywords', String(255), comment='标签(关键词)'),
    Column('purchase_notice', Text, comment='购买须知'),
    Column('features', Text, comment='商品特色'),
    Column('unit', String(20), comment='单位/比如: 份/瓶/箱/斤'),
    Column('weight', Numeric(10, 2), comment='商品重量(kg)'),
    Column('market_price', Numeric(10, 2), comment='市场价'),
    Column('price', Numeric(10, 2), comment='价格'),
    Column('tax_rate', Numeric(5, 2), comment='税率'),
    Column('points_required', Integer, comment='需要积分'),
    Column('points_reward', Integer, comment='赠送积分'),
    Column('min_purchase_qty', Integer, comment='最少购买'),
    Column('stock', Integer, comment='库存'),
    Column('stock_alert', Integer, comment='库存预警'),
    Column('no_stock_mode', Boolean, default=False, comment='无库存'),
    Column('auto_offline', Boolean, default=False, comment='自动下架'),
    Column('member_card_id', String(64), comment='自动发卡'),
    Column('freight_template_id', Integer, comment='运送物流模板'),
    Column('extend_freight_template_id', Integer, comment='扩展物流模板'),
    Column('discount', String(20), comment='优惠券'),
    Column('sort_order', Integer, comment='排序'),
    Column('is_recommended', Boolean, default=False, comment='是否推荐'),
    Column('display_mode', Enum('正常展示', '默认隐藏，不在前端显示'), comment='是否展示'),
    Column('status', Enum('上架', '下架'), comment='状态'),
    Column('video_code', String(128), comment='视频编号'),
    Column('video_url', Text, comment='视频地址'),
    Column('detail', Text, comment='详细介绍'),
    Column('images', JsonText, comment='商品图片(JSON格式，包含多张图片URL)'),
    Column('specifications', Text, comment='商品规格(JSON格式，包含规格名称和规格值)'),
    Column('services', Text, comment='售后服务(JSON格式，包含服务类型和适用状态)'),
    Column('attributes', Text, comment='扩展属性(JSON格式，包含属性名和属性值)'),
    Column('spec_combinations', Text, comment='规格组合(JSON格式，包含初始方式/颜色/尺寸等搭配)'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新者'),
    Column('store_id', Integer, comment='店铺ID'),

)

mapper_registry.map_imperatively(ShopProduct, shop_product_table)

mapper_registry.map_imperatively(ShopProductCategory, product_category_table)


class ShopProductCategorySQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopProductCategory]:
        return ShopProductCategory

    @property
    def query_params(self) -> Tuple:
        return 'name', 'code', 'type', 'parent_id'


class ShopProductSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopProduct]:
        return ShopProduct

    @property
    def query_params(self) -> Tuple:
        return 'status', 'type','category_id','name', 'code',

    # @property
    # def fuzzy_query_params(self) -> Tuple:
    #     return 'name', 'code',


