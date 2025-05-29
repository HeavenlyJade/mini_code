from dataclasses import field
from decimal import Decimal
import datetime as dt
from marshmallow_dataclass import dataclass

from kit.domain.entity import EntityInt


@dataclass
class Distribution(EntityInt):
    sn: str = field(default=None, metadata=dict(description='编号'))
    real_name: str = field(default=None, metadata=dict(description='真实姓名'))
    mobile: str = field(default=None, metadata=dict(description='手机号'))
    identity: int = field(default=None, metadata=dict(description='身份'))
    reason: int = field(default=None, metadata=dict(description='原因'))
    user_id: str = field(default=None, metadata=dict(description='用户ID'))
    wait_amount: float = field(default=None, metadata=dict(description='待提现金额'))
    total_amount: float = field(default=None, metadata=dict(description='总金额'))
    withdrawn_amount: float = field(default=None, metadata=dict(description='已提现金额'))
    wait_deposit_amount:float = field(default=None, metadata=dict(description='等待客户收货确认的入账金额'))
    user_father_id: str = field(default=None, metadata=dict(description='上级ID'))
    user_father_invite_code:str = field(default=None, metadata=dict(description='上级的父亲的邀请码'))
    grade_id: int = field(default=None, metadata=dict(description='等级ID'))
    remark: str = field(default=None, metadata=dict(description='备注'))
    status: int = field(default=None, metadata=dict(description='状态 (0-未审核, 1-已审核)'))
    audit_time: dt.datetime  = field(default=None, metadata=dict(description='审核时间'))
    lv_id: int = field(default=None, metadata=dict(description='用户的分销等级ID'))



@dataclass
class DistributionConfig(EntityInt):
    key: str = field(default=None, metadata=dict(description='配置项'))
    remake: str = field(default=None, metadata=dict(description=''))
    value: str = field(default=None, metadata=dict(description='配置值'))
    content: str = field(default=None, metadata=dict(description='內容'))
    title: str = field(default=None, metadata=dict(description='标题'))


@dataclass
class DistributionGrade(EntityInt):
    name: str = field(default=None, metadata=dict(description='等级名称'))
    weight: int = field(default=None, metadata=dict(description='权重'))
    self_ratio: Decimal = field(default=None, metadata=dict(description='自购比例'))
    first_ratio: Decimal = field(default=None, metadata=dict(description='一级分拥比例'))
    second_ratio: Decimal = field(default=None, metadata=dict(description='二级分拥比例'))
    conditions: float = field(default=None, metadata=dict(description='等级条件'))
    remark: str = field(default=None, metadata=dict(description='备注'))
    update_relation: int = field(default=None, metadata=dict(description='分销关系'))


@dataclass
class DistributionGradeUpdate(EntityInt):
    grade_id: int = field(default=None, metadata=dict(description='等级ID'))
    key: str = field(default=None, metadata=dict(description='条件名称'))
    remake: str = field(default=None, metadata=dict(description=''))
    value: float = field(default=None, metadata=dict(description='条件值'))


@dataclass
class DistributionIncome(EntityInt):
    user_id: str = field(default=None, metadata=dict(description='用户ID'))
    order_id: str = field(default=None, metadata=dict(description='订单ID'))
    order_product_id: str = field(default=None, metadata=dict(description='产品订单ID'))
    product_id: str = field(default=None, metadata=dict(description='产品ID'))
    product_name: str = field(default=None, metadata=dict(description='产品名称'))
    item_id: str = field(default=None, metadata=dict(description='商品ID'))
    money: float = field(default=None, metadata=dict(description='金额'))
    grade_id: int = field(default=None, metadata=dict(description='分销等级ID'))
    level: int = field(default=None, metadata=dict(description='分销层级'))
    ratio: float = field(default=None, metadata=dict(description='分销比例'))
    status: int = field(default=None, metadata=dict(description='状态,0：待结算，2:已结算,3冻结'))
    settlement_time: int = field(default=None, metadata=dict(description='结算时间'))


@dataclass
class DistributionLog(EntityInt):
    distribution_id: int = field(default=None, metadata=dict(description='分销ID'))
    change_object: str = field(default=None, metadata=dict(description='变更对象'))
    change_type: str = field(default=None, metadata=dict(description='变更类型'))
    source_id: int = field(default=None, metadata=dict(description='来源ID'))
    action: str = field(default=None, metadata=dict(description='操作'))
    before_amount: float = field(default=None, metadata=dict(description='变更前金额'))
    left_amount: float = field(default=None, metadata=dict(description='剩余金额'))
    source_sn: str = field(default=None, metadata=dict(description='来源单号'))
    extra: str = field(default=None, metadata=dict(description='额外信息'))
    admin_id: int = field(default=None, metadata=dict(description='管理员ID'))
    user_id: str = field(default=None, metadata=dict(description='管理员ID'))
