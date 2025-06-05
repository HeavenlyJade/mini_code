from dataclasses import field
from typing import Optional
from decimal import Decimal
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopStore(Entity):
    """
    商店领域模型

    用于表示商店的基本信息，包括名称、类型、地址、联系方式等属性
    """
    name: str = field(
        default=None,
        metadata=dict(
            description='商店名称',
        ),
    )
    type: str = field(
        default=None,
        metadata=dict(
            description='商店类型',
        ),
    )
    store_code: str = field(
        default=None,
        metadata=dict(
            description='门店编号',
        ),
    )
    fresh_delivery: str = field(
        default=None,
        metadata=dict(
            description='生鲜配送',
        ),
    )
    receive_method: str = field(
        default=None,
        metadata=dict(
            description='接单模式',
        ),
    )
    takeout_enabled: bool = field(
        default=False,
        metadata=dict(
            description='外卖模式',
        ),
    )
    self_pickup_enabled: bool = field(
        default=False,
        metadata=dict(
            description='自取模式',
        ),
    )
    dine_in_enabled: bool = field(
        default=False,
        metadata=dict(
            description='堂食模式',
        ),
    )
    store_category: int = field(
        default=None,
        metadata=dict(
            description='门店分类ID',
        ),
    )
    province: str = field(
        default=None,
        metadata=dict(
            description='省市区',
        ),
    )
    province_code: str = field(
        default=None,
        metadata=dict(
            description='省市区编码',
        ),
    )
    address: str = field(
        default=None,
        metadata=dict(
            description='地址',
        ),
    )
    contact_person: str = field(
        default=None,
        metadata=dict(
            description='联系人',
        ),
    )
    contact_phone: str = field(
        default=None,
        metadata=dict(
            description='联系电话',
        ),
    )
    is_public: bool = field(
        default=False,
        metadata=dict(
            description='是否公开服务方式',
        ),
    )
    qq: str = field(
        default=None,
        metadata=dict(
            description='QQ',
        ),
    )
    service_fee_rate: float = field(
        default=None,
        metadata=dict(
            description='服务费率',
        ),
    )
    gst_tax_rate: float = field(
        default=None,
        metadata=dict(
            description='GST消费税率',
        ),
    )
    print_config: str = field(
        default=None,
        metadata=dict(
            description='打印打单',
        ),
    )
    wechat_config: str = field(
        default=None,
        metadata=dict(
            description='企业微信通知',
        ),
    )
    business_scope: str = field(
        default=None,
        metadata=dict(
            description='经营范围',
        ),
    )
    description: str = field(
        default=None,
        metadata=dict(
            description='介绍',
        ),
    )
    features: str = field(
        default=None,
        metadata=dict(
            description='特色',
        ),
    )
    latitude: float = field(
        default=None,
        metadata=dict(
            description='地理位置纬度',
        ),
    )
    longitude: float = field(
        default=None,
        metadata=dict(
            description='地理位置经度',
        ),
    )
    sort_order: int = field(
        default=None,
        metadata=dict(
            description='排序',
        ),
    )
    status: str = field(
        default=None,
        metadata=dict(
            description='状态',
        ),
    )
    store_logo: str = field(
        default=None,
        metadata=dict(
            description='商店Logo',
        ),
    )
    store_image: str = field(
        default=None,
        metadata=dict(
            description='商店图片',
        ),
    )
    opening_hours: str = field(
        default=None,
        metadata=dict(
            description='营业时间',
        ),
    )
    delivery_price: float = field(
        default=None,
        metadata=dict(
            description='配送价格',
        ),
    )
    min_order_amount: float = field(
        default=None,
        metadata=dict(
            description='最小订单金额',
        ),
    )
    door_info: str = field(
        default=None,
        metadata=dict(
            description='门店信息',
        ),
    )
    wifi_name: str = field(
        default=None,
        metadata=dict(
            description='WiFi名称',
        ),
    )
    wifi_password: str = field(
        default=None,
        metadata=dict(
            description='WiFi密码',
        ),
    )
    customer_notice: str = field(
        default=None,
        metadata=dict(
            description='客户须知',
        ),
    )
