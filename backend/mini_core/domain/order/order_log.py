import datetime as dt
from dataclasses import field
from typing import Optional,Dict,Union,Any
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity
from kit.domain.types import DateTimeField, StrField


@dataclass
class OrderLog(Entity):
    """
    订单日志领域模型

    用于记录订单的各种操作日志，包括操作类型、操作描述、操作人、操作时间等
    """
    order_no: str = field(
        default=None,
        metadata=dict(
            description='订单编号',
        ),
    )
    operation_type: str = field(
        default=None,
        metadata=dict(
            description='操作类型',
        ),
    )
    operation_desc: str = field(
        default=None,
        metadata=dict(
            description='操作描述',
        ),
    )
    operator: str = field(
        default=None,
        metadata=dict(
            description='操作人',
        ),
    )
    operation_time: DateTimeField = field(
        default_factory=dt.datetime.now,
        metadata=dict(
            description='操作时间',
        ),
    )
    operation_ip: str = field(
        default=None,
        metadata=dict(
            description='操作IP',
        ),
    )
    old_value:Any = field(
        default=None,
        metadata=dict(
            description='修改前值',
        ),
    )
    new_value: Any = field(
        default=None,
        metadata=dict(
            description='修改后值',
        ),
    )
    remark: Optional[str] = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
    updater: Optional[str] = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
