import datetime as dt
from dataclasses import dataclass, field

from kit.domain.entity import Entity
from kit.domain.field import ExtendedIntEnum
from kit.domain.types import StrField

__all__ = ['Log', 'LogOperatingType']


class LogOperatingType(ExtendedIntEnum):
    """日志类型"""

    LOGIN = 1
    OPERATION = 2
    TUNING_PARA = 3
    ERROR = 4

    @classmethod
    def comparison_map(cls) -> dict:
        return {1: '登入登出', 2: '操作', 3: '调参记录', 4: '报错日志'}


@dataclass
class Log(Entity):
    operating_user: StrField = field(
        default=None,
        metadata=dict(
            required=True,
            description='操作用户',
        ),
    )
    operating_type: int = field(
        default=None,
        metadata=dict(
            required=True,
            description=LogOperatingType.desc(),
        ),
    )
    operating_detail: str = field(
        default=None,
        metadata=dict(
            required=True,
            description='操作详情',
        ),
    )
    operating_time: dt.datetime = field(
        init=False,
        metadata=dict(
            dump_only=True,
        ),
    )
