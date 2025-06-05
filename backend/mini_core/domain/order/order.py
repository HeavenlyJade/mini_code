from dataclasses import field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopOrder(Entity):
    """
    订单领域模型

    用于表示订单的基本信息，包括订单号、用户信息、商品信息、配送信息、支付信息等
    """
    order_no: str = field(
        default=None,
        metadata=dict(
            description='订单编号',
        ),
    )
    order_sn: str = field(
        default=None,
        metadata=dict(
            description='订单号',
        ),
    )
    product_name: str = field(
        default=None,
        metadata=dict(
            description='商品组合名称',
        ),
    )
    user_id: str = field(
        default=None,
        metadata=dict(
            description='用户编号',
        ),
    )
    nickname: str = field(
        default=None,
        metadata=dict(
            description='用户昵称',
        ),
    )
    phone: str = field(
        default=None,
        metadata=dict(
            description='用户手机号',
        ),
    )
    order_type: str = field(
        default=None,
        metadata=dict(
            description='订单类型(普通订单/套餐订单等)',
        ),
    )
    order_source: str = field(
        default=None,
        metadata=dict(
            description='订单来源',
        ),
    )
    status: str = field(
        default=None,
        metadata=dict(
            description='订单状态',
        ),
    )
    refund_status: str = field(
        default=None,
        metadata=dict(
            description='退款状态',
        ),
    )
    delivery_status: str = field(
        default=None,
        metadata=dict(
            description='配送状态',
        ),
    )
    payment_status: str = field(
        default=None,
        metadata=dict(
            description='支付状态',
        ),
    )
    product_count: int = field(
        default=None,
        metadata=dict(
            description='商品数量',
        ),
    )
    product_amount: float = field(
        default=None,
        metadata=dict(
            description='商品金额',
        ),
    )
    actual_amount: float = field(
        default=None,
        metadata=dict(
            description='实收金额',
        ),
    )
    discount_amount: float = field(
        default=None,
        metadata=dict(
            description='优惠金额',
        ),
    )
    freight_amount: float = field(
        default=None,
        metadata=dict(
            description='运费金额',
        ),
    )
    point_amount: int = field(
        default=None,
        metadata=dict(
            description='积分抵扣',
        ),
    )
    pay_method: str = field(
        default=None,
        metadata=dict(
            description='支付方式',
        ),
    )
    payment_no: str = field(
        default=None,
        metadata=dict(
            description='支付单号',
        ),
    )
    trade_no: str = field(
        default=None,
        metadata=dict(
            description='交易号',
        ),
    )

    receiver_name: str = field(
        default=None,
        metadata=dict(
            description='收货人姓名',
        ),
    )
    receiver_phone: str = field(
        default=None,
        metadata=dict(
            description='收货人电话',
        ),
    )
    province: str = field(
        default=None,
        metadata=dict(
            description='省份',
        ),
    )
    city: str = field(
        default=None,
        metadata=dict(
            description='城市',
        ),
    )
    district: str = field(
        default=None,
        metadata=dict(
            description='区/县',
        ),
    )
    address: str = field(
        default=None,
        metadata=dict(
            description='详细地址',
        ),
    )
    postal_code: str = field(
        default=None,
        metadata=dict(
            description='邮编',
        ),
    )
    id_card_no: str = field(
        default=None,
        metadata=dict(
            description='身份证号码',
        ),
    )
    express_company: str = field(
        default=None,
        metadata=dict(
            description='快递公司名称',
        ),
    )
    express_no: str = field(
        default=None,
        metadata=dict(
            description='快递单号',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
    client_remark: str = field(
        default=None,
        metadata=dict(
            description='客户备注',
        ),
    )
    transaction_time: datetime = field(
        default=None,
        metadata=dict(
            description='交易时间',
        ),
    )
    payment_time: datetime = field(
        default=None,
        metadata=dict(
            description='支付时间',
        ),
    )
    ship_time: datetime = field(
        default=None,
        metadata=dict(
            description='发货时间',
        ),
    )
    confirm_time: datetime = field(
        default=None,
        metadata=dict(
            description='确认收货时间',
        ),
    )
    close_time: datetime = field(
        default=None,
        metadata=dict(
            description='交易关闭时间',
        ),
    )
    buyer_ip: str = field(
        default=None,
        metadata=dict(
            description='下单IP',
        ),
    )
    delivery_platform: str = field(
        default=None,
        metadata=dict(
            description='配送平台',
        ),
    )
    delivery_status_desc: str = field(
        default=None,
        metadata=dict(
            description='配送状态描述',
        ),
    )
    pre_sale_time: datetime = field(
        default=None,
        metadata=dict(
            description='预售日期',
        ),
    )
    parent_order_id: int = field(
        default=None,
        metadata=dict(
            description='父订单ID',
        ),
    )
    external_order_no: str = field(
        default=None,
        metadata=dict(
            description='外部订单号',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
