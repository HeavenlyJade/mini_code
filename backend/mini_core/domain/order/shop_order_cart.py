from dataclasses import field
from typing import Optional
from datetime import datetime
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopOrderCart(Entity):
    """
    购物车领域模型

    用于表示用户的购物车信息，包括用户ID、商品信息、数量等
    """
    user_id: str = field(
        default=None,
        metadata=dict(
            description='用户ID',
        ),
    )
    open_id: str = field(
        default=None,
        metadata=dict(
            description='微信openID',
        ),
    )
    sku_id: int = field(
        default=None,
        metadata=dict(
            description='商品SKU ID',
        ),
    )
    product_count: int = field(
        default=None,
        metadata=dict(
            description='商品数量',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
