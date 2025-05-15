from dataclasses import field
from typing import Optional
from marshmallow_dataclass import dataclass
from datetime import datetime

from kit.domain.entity import Entity


@dataclass
class OrderReview(Entity):
    """
    订单评价领域模型

    用于表示用户对订单商品的评价信息，包括评分、评价内容、图片等
    """
    order_no: str = field(
        default=None,
        metadata=dict(
            description='订单编号',
        ),
    )
    order_detail_id: str = field(
        default=None,
        metadata=dict(
            description='订单详情ID',
        ),
    )
    product_id: int = field(
        default=None,
        metadata=dict(
            description='商品ID',
        ),
    )
    user_id: str = field(
        default=None,
        metadata=dict(
            description='用户ID',
        ),
    )
    nickname: str = field(
        default=None,
        metadata=dict(
            description='用户昵称',
        ),
    )
    avatar: str = field(
        default=None,
        metadata=dict(
            description='用户头像',
        ),
    )
    rating: int = field(
        default=5,
        metadata=dict(
            description='评分(1-5)',
        ),
    )
    content: str = field(
        default=None,
        metadata=dict(
            description='评价内容',
        ),
    )
    images: str = field(
        default=None,
        metadata=dict(
            description='评价图片(JSON字符串，存储图片URL列表)',
        ),
    )
    is_anonymous: bool = field(
        default=False,
        metadata=dict(
            description='是否匿名评价',
        ),
    )
    status: str = field(
        default='已发布',
        metadata=dict(
            description='评价状态(审核中/已发布/已屏蔽)',
        ),
    )
    is_top: bool = field(
        default=False,
        metadata=dict(
            description='是否置顶',
        ),
    )
    review_time: datetime = field(
        default=None,
        metadata=dict(
            description='评价时间',
        ),
    )
    reply_content: str = field(
        default=None,
        metadata=dict(
            description='商家回复内容',
        ),
    )
    reply_time: datetime = field(
        default=None,
        metadata=dict(
            description='商家回复时间',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
