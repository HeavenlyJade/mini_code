from dataclasses import field
from typing import Optional
from decimal import Decimal
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopOrderSetting(Entity):
    """
    订单配置领域模型

    用于表示商店的订单相关配置，包括自动关闭时间、自动收货天数、物流超时时间等
    """
    shop_id: int = field(
        default=None,
        metadata=dict(
            description='店铺ID',
        ),
    )
    auto_close_minutes: int = field(
        default=None,
        metadata=dict(
            description='自动关闭(下单N分钟后未支付自动关闭订单)',
        ),
    )
    auto_receive_days: int = field(
        default=None,
        metadata=dict(
            description='自动收货(发货后超过N天用户未确认,收货自动确认收货)',
        ),
    )
    logistics_timeout_hours: int = field(
        default=None,
        metadata=dict(
            description='物流动态超时时未更新提醒(0代表不提醒)',
        ),
    )
    points_rate: Decimal = field(
        default=None,
        metadata=dict(
            description='积分抵扣比例(1元等于多少积分)',
        ),
    )
    invoice_contact_phone: str = field(
        default=None,
        metadata=dict(
            description='联系电话',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
