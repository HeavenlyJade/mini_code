from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, date
from marshmallow_dataclass import dataclass as ma_dataclass

from kit.domain.entity import Entity


@ma_dataclass
class ShopUser(Entity):
    """商城用户领域模型"""
    user_id: str = field(
        default=None,
        metadata=dict(
            description='用户编号',
        ),
    )
    username: str = field(
        default=None,
        metadata=dict(
            description='用户名',
        ),
    )
    nickname: str = field(
        default=None,
        metadata=dict(
            description='昵称',
        ),
    )
    phone: str = field(
        default=None,
        metadata=dict(
            description='手机号码',
        ),
    )
    email: str = field(
        default=None,
        metadata=dict(
            description='邮箱地址',
        ),
    )
    password: str = field(
        default=None,
        metadata=dict(
            description='登录密码(加密存储)',
            load_only=True,
        ),
    )
    avatar: str = field(
        default=None,
        metadata=dict(
            description='头像URL',
        ),
    )
    openid: str = field(
        default=None,
        metadata=dict(
            description='微信openid',
        ),
    )
    unionid: str = field(
        default=None,
        metadata=dict(
            description='微信unionid',
        ),
    )
    mini_program_name: str = field(
        default=None,
        metadata=dict(
            description='小程序名称',
        ),
    )
    register_channel: str = field(
        default=None,
        metadata=dict(
            description='注册渠道',
        ),
    )
    register_shop_id: int = field(
        default=None,
        metadata=dict(
            description='所属门店ID',
        ),
    )
    register_shop_name: str = field(
        default=None,
        metadata=dict(
            description='所属门店名称',
        ),
    )
    real_name: str = field(
        default=None,
        metadata=dict(
            description='真实姓名',
        ),
    )
    gender: int = field(
        default=None,
        metadata=dict(
            description='性别(0-未知,1-男,2-女)',
        ),
    )
    birthday: date = field(
        default=None,
        metadata=dict(
            description='生日',
        ),
    )
    address: str = field(
        default=None,
        metadata=dict(
            description='详细地址',
        ),
    )
    member_level: str = field(
        default=None,
        metadata=dict(
            description='会员等级',
        ),
    )
    member_card_no: str = field(
        default=None,
        metadata=dict(
            description='会员卡号',
        ),
    )
    points: int = field(
        default=None,
        metadata=dict(
            description='积分',
        ),
    )
    balance: float = field(
        default=None,
        metadata=dict(
            description='账户余额',
        ),
    )
    is_distributor: int = field(
        default=0,
        metadata=dict(
            description='是否分销商(1-是,0-否)',
        ),
    )
    tags: str = field(
        default=None,
        metadata=dict(
            description='标签(多个用逗号分隔)',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
    status: int = field(
        default=1,
        metadata=dict(
            description='状态(1-正常,0-停用)',
        ),
    )
    last_login_time: datetime = field(
        default=None,
        metadata=dict(
            description='最后登录时间',
        ),
    )
    last_login_ip: str = field(
        default=None,
        metadata=dict(
            description='最后登录IP',
        ),
    )
    register_time: datetime = field(
        default=None,
        metadata=dict(
            description='成为会员时间',
        ),
    )
    register_ip: str = field(
        default=None,
        metadata=dict(
            description='注册IP',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
    invite_code: str = field(
        default=None,
        metadata=dict(
            description='邀请吗',
        ),
    )


@ma_dataclass
class ShopUserAddress(Entity):
    """商城用户地址领域模型"""
    user_id: str = field(
        default=None,
        metadata=dict(
            description='用户编号',
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
    detail_address: str = field(
        default=None,
        metadata=dict(
            description='详细地址',
        ),
    )
    postal_code: str = field(
        default=None,
        metadata=dict(
            description='邮政编码',
        ),
    )
    is_default: int = field(
        default=0,
        metadata=dict(
            description='是否默认地址(1-是,0-否)',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )

