# -*- coding: utf-8 -*-
# author zyy
from dataclasses import field

from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity

__all__ = ['License']


@dataclass
class License(Entity):
    customer_name: str = field(
        default=None,
        metadata=dict(
            description='客户名称',
        ),
    )
    unique_code: str = field(
        default=None,
        metadata=dict(
            description='设备唯一识别码',
        ),
    )
    license: str = field(
        default=None,
        metadata=dict(
            description='license',
        ),
    )
    start_time: str = field(
        default=None,
        metadata=dict(
            description='start_time',
        ),
    )
    end_time: str = field(
        default=None,
        metadata=dict(
            description='end_time',
        ),
    )
    is_del: int = field(
        default=0,
        metadata=dict(
            description='是否删除 0 正常 1 删除',
        ),
    )

