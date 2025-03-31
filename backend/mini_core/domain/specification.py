from dataclasses import field
from typing import Optional,List,Dict
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopSpecification(Entity):
    """
    商品规格领域模型

    用于表示商品的规格信息，包括规格名称、备注、排序等属性
    """
    name: str = field(
        default=None,
        metadata=dict(
            description='规格名称',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
    sort_order: int = field(
        default=None,
        metadata=dict(
            description='排序',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新者',
        ),
    )


@dataclass
class ShopSpecificationAttribute(Entity):
    """
    商品规格属性领域模型

    用于表示商品规格的具体属性值，包括属性名称、属性值、备注等
    """
    specification_id: int = field(
        default=None,
        metadata=dict(
            description='规格ID',
        ),
    )
    name: str = field(
        default=None,
        metadata=dict(
            description='属性名称',
        ),
    )
    attribute_value: dict = field(
        default_factory=dict,  # 使用default_factory=dict而不是default=None
        metadata=dict(
            description='属性内容',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
    sort_order: int = field(
        default=None,
        metadata=dict(
            description='排序',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新者',
        ),
    )
