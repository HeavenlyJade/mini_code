import datetime as dt
import uuid
from dataclasses import dataclass, field
from typing import Optional

from kit.domain.entity import Entity
from kit.domain.types import DateTimeField, StrField

__all__ = ['Alarm']


@dataclass
class Alarm(Entity):
    message: str = field(default=None, metadata=dict(required=True, description='报警信息'))
    alarm_time: DateTimeField = field(
        default_factory=dt.datetime.now,
        metadata=dict(
            dump_only=True,
        ),
    )
    task_id: StrField = field(
        default=None,
    )
    context: Optional[dict] = field(
        default_factory=dict,
    )
    flow_name: StrField = field(
        default=None,
        metadata=dict(dump_only=True)
    )
    version_number: StrField = field(
        default=None,
        metadata=dict(dump_only=True)
    )
    eqp_area: StrField = field(
        default=None,
        metadata=dict(dump_only=True)
    )
    flow_id: StrField = field(
        default=None,
        metadata=dict(dump_only=True)
    )
