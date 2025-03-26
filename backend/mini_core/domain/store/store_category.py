from dataclasses import field
from typing import Optional
from marshmallow_dataclass import dataclass

from kit.domain.entity import Entity


@dataclass
class ShopStoreCategory(Entity):
    """
    商店分类领域模型

    用于表示商店中的分类信息，包括分类名称、编码、上级分类、图标、排序等属性
    可用于构建商店分类的层级结构
    """
    name: str = field(
        default=None,
        metadata=dict(
            description='分类名称',
        ),
    )
    code: str = field(
        default=None,
        metadata=dict(
            description='分类编码',
        ),
    )
    parent_id: int = field(
        default=None,
        metadata=dict(
            description='上级分类ID',
        ),
    )
    icon: str = field(
        default=None,
        metadata=dict(
            description='图标路径',
        ),
    )
    image: str = field(
        default=None,
        metadata=dict(
            description='图片路径',
        ),
    )
    sort_order: int = field(
        default=None,
        metadata=dict(
            description='排序',
        ),
    )
    status: str = field(
        default=None,
        metadata=dict(
            description='状态',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注说明',
        ),
    )
    is_recommend: bool = field(
        default=False,
        metadata=dict(
            description='是否推荐',
        ),
    )
