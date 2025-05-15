from dataclasses import field
from typing import Optional
from datetime import datetime
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopOrderLogistics(Entity):
    """
    订单物流领域模型

    用于表示订单的物流配送信息，包括物流单号、物流公司、发送方信息、接收方信息、物流路线等
    """
    order_no: str = field(
        default=None,
        metadata=dict(
            description='订单编号',
        ),
    )
    logistics_no: str = field(
        default=None,
        metadata=dict(
            description='物流单号',
        ),
    )
    logistics_company: str = field(
        default=None,
        metadata=dict(
            description='物流公司',
        ),
    )
    logistics_code: str = field(
        default=None,
        metadata=dict(
            description='物流公司编码',
        ),
    ),
    courier_number: str = field(
        default=None,
        metadata=dict(
            description='快递员编号',
        ),
    )
    courier_phone: str = field(
        default=None,
        metadata=dict(
            description='快递员电话',
        ),
    )
    sender_info: str = field(
        default=None,
        metadata=dict(
            description='发件人信息(JSON格式)',
        ),
    )
    receiver_info: str = field(
        default=None,
        metadata=dict(
            description='收件人信息(JSON格式)',
        ),
    )
    shipping_time: datetime = field(
        default=None,
        metadata=dict(
            description='发货时间',
        ),
    )
    estimate_time: datetime = field(
        default=None,
        metadata=dict(
            description='预计送达时间',
        ),
    )
    receiving_time: datetime = field(
        default=None,
        metadata=dict(
            description='实际收货时间',
        ),
    )
    current_status: str = field(
        default=None,
        metadata=dict(
            description='当前状态',
        ),
    )
    current_location: str = field(
        default=None,
        metadata=dict(
            description='当前位置',
        ),
    )
    logistics_route: str = field(
        default=None,
        metadata=dict(
            description='物流轨迹(JSON格式)',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
    start_date: datetime = field(
        default=None,
        metadata=dict(
            description='记录开始时间(用于控制表)',
        ),
    )
    end_date: datetime = field(
        default=None,
        metadata=dict(
            description='记录结束时间(用于控制表)',
        ),
    )
