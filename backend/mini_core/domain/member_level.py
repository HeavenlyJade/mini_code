from dataclasses import field
from decimal import Decimal
from typing import Optional
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class MemberLevelConfig(Entity):
    """
    会员等级配置领域模型

    用于表示会员等级的配置信息，包括等级代码、名称、升级条件、权益等
    """
    level_code: str = field(
        default=None,
        metadata=dict(
            description='等级代码（如：LV0, LV1, LV2...）',
        ),
    )
    level_name: str = field(
        default=None,
        metadata=dict(
            description='等级名称（如：普通会员、银牌会员、金牌会员...）',
        ),
    )
    level_value: int = field(
        default=None,
        metadata=dict(
            description='等级数值（用于排序和比较）',
        ),
    )
    upgrade_condition_type: int = field(
        default=1,
        metadata=dict(
            description='升级条件类型：1-消费金额 2-消费次数 3-邀请人数 4-手动设置',
        ),
    )
    upgrade_amount: Decimal = field(
        default=None,
        metadata=dict(
            description='升级所需消费金额',
        ),
    )
    upgrade_count: int = field(
        default=0,
        metadata=dict(
            description='升级所需消费次数',
        ),
    )
    upgrade_invite_count: int = field(
        default=0,
        metadata=dict(
            description='升级所需邀请人数',
        ),
    )
    discount_rate: Decimal = field(
        default=None,
        metadata=dict(
            description='会员折扣率（如：95.00表示95折）',
        ),
    )
    point_ratio: Decimal = field(
        default=None,
        metadata=dict(
            description='积分倍率（如：1.5表示1.5倍积分）',
        ),
    )
    level_icon: Optional[str] = field(
        default=None,
        metadata=dict(
            description='等级图标URL',
        ),
    )
    level_color: Optional[str] = field(
        default=None,
        metadata=dict(
            description='等级颜色（用于前端展示）',
        ),
    )
    level_description: Optional[str] = field(
        default=None,
        metadata=dict(
            description='等级描述',
        ),
    )
    benefits: Optional[str] = field(
        default=None,
        metadata=dict(
            description='会员权益（JSON格式存储）',
        ),
    )
    is_enabled: bool = field(
        default=True,
        metadata=dict(
            description='是否启用',
        ),
    )
    sort_order: int = field(
        default=0,
        metadata=dict(
            description='排序（数字越小越靠前）',
        ),
    )
    creator: Optional[str] = field(
        default=None,
        metadata=dict(
            description='创建人',
        ),
    )
    updater: Optional[str] = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
