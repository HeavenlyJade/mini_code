# backend/business/domain/banner_sqla.py
from dataclasses import field
from marshmallow_dataclass import dataclass
from kit.domain.entity import Entity


@dataclass
class Banner(Entity):
    """
    Banner领域模型

    用于表示网站或应用的横幅广告信息
    """
    code_type: str = field(
        default=None,
        metadata=dict(
            description='自定义类型',
        ),
    )
    business_code: str = field(
        default='0',
        metadata=dict(
            description='业务编号',
        ),
    )
    name: str = field(
        default=None,
        metadata=dict(
            description='横幅名称',
        ),
    )
    upload_image: str = field(
        default=None,
        metadata=dict(
            description='上传图片路径',
        ),
    ),
    upload_video: str = field(
        default=None,
        metadata=dict(
            description='上传视频路径',
        ),
    )
    expand_image: str = field(
        default=None,
        metadata=dict(
            description='扩展图片路径',
        ),
    )
    link_type: str = field(
        default=None,
        metadata=dict(
            description='链接类型',
        ),
    )
    link_url: str = field(
        default=None,
        metadata=dict(
            description='链接地址',
        ),
    )
    remark: str = field(
        default=None,
        metadata=dict(
            description='备注',
        ),
    )
    status: int = field(
        default=1,
        metadata=dict(
            description='状态(1-显示,0-隐藏)',
        ),
    )
    sort_order: int = field(
        default=10,
        metadata=dict(
            description='排序',
        ),
    )
    creator: str = field(
        default=None,
        metadata=dict(
            description='创建人',
        ),
    )
    updater: str = field(
        default=None,
        metadata=dict(
            description='更新人',
        ),
    )
