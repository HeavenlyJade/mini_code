from dataclasses import field
from typing import Optional
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopReturnReason(Entity):
    """
    退货原因领域模型

    用于表示商店的退货原因类型配置，包括原因类型、排序和是否启用等
    """
    reason_type: str = field(
        default=None,
        metadata=dict(
            description='原因类型',
        ),
    )
    sort_order: int = field(
        default=1,
        metadata=dict(
            description='排序',
        ),
    )
    is_enabled: bool = field(
        default=True,
        metadata=dict(
            description='是否可用',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
