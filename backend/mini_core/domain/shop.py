from dataclasses import field
from typing import Optional
from decimal import Decimal
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity, EntityInt


@dataclass
class ShopProductCategory(Entity):
    name: str = field(default=None, metadata=dict(description='分类名称'))
    remark: str = field(default=None, metadata=dict(description='备注'))
    type: str = field(default=None, metadata=dict(description='类型'))
    parent_id: int = field(default=None, metadata=dict(description='上级分类ID'))
    code: str = field(default=None, metadata=dict(description='编号'))
    icon: str = field(default=None, metadata=dict(description='图标路径'))
    image: str = field(default=None, metadata=dict(description='图片路径'))
    sort_order: int = field(default=None, metadata=dict(description='排序'))
    status: str = field(default=None, metadata=dict(description='状态'))
    is_audit: bool = field(default=False, metadata=dict(description='是否审核'))
    audit_type: str = field(default=None, metadata=dict(description='审核类型'))
    store_id: int = field(default=None, metadata=dict(description='所属门店ID'))


@dataclass
class ShopProduct(EntityInt):
    category_id: int = field(default=None, metadata=dict(description='商品分类ID'))
    code: str = field(default=None, metadata=dict(description='商品编号'))
    name: str = field(default=None, metadata=dict(description='商品名称'))
    alias: str = field(default=None, metadata=dict(description='别名'))
    type: str = field(default=None, metadata=dict(description='类型'))
    support_overseas_shipping: bool = field(default=False, metadata=dict(description='是否支持海外直邮'))
    keywords: str = field(default=None, metadata=dict(description='标签(关键词)'))
    purchase_notice: str = field(default=None, metadata=dict(description='购买须知'))
    features: str = field(default=None, metadata=dict(description='商品特色'))
    unit: str = field(default=None, metadata=dict(description='单位/比如: 份/瓶/箱/斤'))
    weight: Decimal = field(default=None, metadata=dict(description='商品重量(kg)'))
    market_price: Decimal = field(default=None, metadata=dict(description='市场价'))
    price: Decimal = field(default=None, metadata=dict(description='价格'))
    tax_rate: Decimal = field(default=None, metadata=dict(description='税率'))
    points_required: int = field(default=None, metadata=dict(description='需要积分'))
    points_reward: int = field(default=None, metadata=dict(description='赠送积分'))
    min_purchase_qty: int = field(default=None, metadata=dict(description='最少购买'))
    stock: int = field(default=None, metadata=dict(description='库存'))
    stock_alert: int = field(default=None, metadata=dict(description='库存预警'))
    no_stock_mode: bool = field(default=False, metadata=dict(description='无库存'))
    auto_offline: bool = field(default=False, metadata=dict(description='自动下架'))
    member_card_id: str = field(default=None, metadata=dict(description='自动发卡'))
    freight_template_id: int = field(default=None, metadata=dict(description='运送物流模板'))
    extend_freight_template_id: int = field(default=None, metadata=dict(description='扩展物流模板'))
    discount: str = field(default=None, metadata=dict(description='优惠券'))
    sort_order: int = field(default=None, metadata=dict(description='排序'))
    is_recommended: bool = field(default=False, metadata=dict(description='是否推荐'))
    display_mode: str = field(default=None, metadata=dict(description='是否展示'))
    status: str = field(default=None, metadata=dict(description='状态'))
    video_code: str = field(default=None, metadata=dict(description='视频编号'))
    video_url: str = field(default=None, metadata=dict(description='视频地址'))
    detail: str = field(default=None, metadata=dict(description='详细介绍'))
    images: str = field(default=None, metadata=dict(description='商品图片(JSON格式，包含多张图片URL)'))
    specifications: str = field(default=None, metadata=dict(description='商品规格(JSON格式，包含规格名称和规格值)'))
    services: str = field(default=None, metadata=dict(description='售后服务(JSON格式，包含服务类型和适用状态)'))
    attributes: str = field(default=None, metadata=dict(description='扩展属性(JSON格式，包含属性名和属性值)'))
    spec_combinations: str = field(default=None, metadata=dict(description='规格组合(JSON格式，包含初始方式/颜色/尺寸等搭配)'))
    updater: str = field(default=None, metadata=dict(description='更新者'))
