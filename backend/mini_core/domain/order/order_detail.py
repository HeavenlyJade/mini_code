from dataclasses import field
from typing import Optional
from decimal import Decimal
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class OrderDetail(Entity):
    """
    订单详情领域模型

    用于表示订单中的商品详情信息，包括订单号、商品信息、价格、数量等
    """
    order_no: str = field(
        default=None,
        metadata=dict(
            description='订单ID',
        ),
    )
    sku_id: str = field(
        default=None,
        metadata=dict(
            description='sku_id',
        ),
    )
    product_id: int = field(
        default=None,
        metadata=dict(
            description='商品ID',
        ),
    )
    sku_code: str = field(
        default=None,
        metadata=dict(
            description='SKU编码',
        ),
    )
    price: Decimal = field(
        default=None,
        metadata=dict(
            description='原价格',
        ),
    )
    actual_price: Decimal = field(
        default=None,
        metadata=dict(
            description='实际购买价格',
        ),
    )
    num: int = field(
        default=None,
        metadata=dict(
            description='购买数量',
        ),
    )
    product_img: str = field(
        default=None,
        metadata=dict(
            description='商品图片',
        ),
    )
    product_spec: str = field(
        default=None,
        metadata=dict(
            description='商品规格',
        ),
    )
    product_name: str = field(
        default=None,
        metadata=dict(
            description='商品名称',
        ),
    )
    quantity: int = field(
        default=None,
        metadata=dict(
            description='商品数量',
        ),
    )
    unit_price: Decimal = field(
        default=None,
        metadata=dict(
            description='商品单价',
        ),
    )
    total_price: Decimal = field(
        default=None,
        metadata=dict(
            description='商品总价',
        ),
    )
    is_gift: int = field(
        default=0,
        metadata=dict(
            description='是否赠品',
        ),
    )
