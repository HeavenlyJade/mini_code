from dataclasses import field
from typing import Optional
from decimal import Decimal
from marshmallow_dataclass import dataclass
import datetime as dt
from kit.domain.entity import Entity


@dataclass
class OrderDetail(Entity):
    """
    订单详情领域模型

    用于表示订单中的商品详情信息，包括订单号、商品信息、价格、数量等 order_item_id
    """
    order_item_id: str = field(
        default=None,
        metadata=dict(
            description='订单订单明细ID',
        ),
    )
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
    price: float = field(
        default=None,
        metadata=dict(
            description='原价格',
        ),
    )
    actual_price: float = field(
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
    unit_price: float = field(
        default=None,
        metadata=dict(
            description='商品单价',
        ),
    )
    total_price: float = field(
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
    refund_status: int = field(
        default=0,
        metadata=dict(
            description='退款状态,0:无退款,1退款中,2，已拒绝,3，已完成',
        ),
    )
    refund_time: dt.datetime = field(
        default=None,
        metadata=dict(
            dump_only=True,
        ),
    )

