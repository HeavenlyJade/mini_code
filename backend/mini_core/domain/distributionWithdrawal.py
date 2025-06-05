
from dataclasses import field

import datetime as dt
from marshmallow_dataclass import dataclass

from kit.domain.entity import EntityInt


@dataclass
class DistributionWithdrawal(EntityInt):
    user_id: str = field(default=None, metadata=dict(description='用户ID'))
    user_name: str = field(default=None, metadata=dict(description='用户名称'))
    withdrawal_no: str = field(default=None, metadata=dict(description='提现申请单号'))
    apply_amount: float= field(default=None, metadata=dict(description='申请提现金额'))
    actual_amount: float = field(default=None, metadata=dict(description='实际到账金额'))
    fee_amount: float = field(default=None, metadata=dict(description='手续费'))
    withdrawal_type: str = field(default=None, metadata=dict(description='提现方式'))
    account_info: str = field(default=None, metadata=dict(description='收款账户信息'))
    status: int = field(default=0, metadata=dict(description='状态'))
    apply_time: dt.datetime = field(default=None, metadata=dict(description='申请时间'))
    audit_time: dt.datetime = field(default=None, metadata=dict(description='审核时间'))
    process_time: dt.datetime = field(default=None, metadata=dict(description='处理时间'))
    complete_time: dt.datetime = field(default=None, metadata=dict(description='完成时间'))
    handler_id: int = field(default=None, metadata=dict(description='处理人ID'))
    handler_name: str = field(default=None, metadata=dict(description='处理人姓名'))
    reject_reason: str = field(default=None, metadata=dict(description='拒绝原因'))
    remark: str = field(default=None, metadata=dict(description='备注'))
    transaction_id: str = field(default=None, metadata=dict(description='第三方交易流水号'))
