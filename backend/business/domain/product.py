from dataclasses import field

from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity

__all__ = ['Product']


@dataclass
class Product(Entity):
    product_name: str = field(
        default=None,
        metadata=dict(
            description='产品名称',
        ),
    )
