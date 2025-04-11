# backend/business/schema/banner_sqla.py
from marshmallow import EXCLUDE
from marshmallow_dataclass import class_schema
from webargs import fields

from backend.mini_core.domain.banner import Banner
from kit.schema.base import (
    ArgSchema,
    EntitySchema,
    ListQueryArgSchema,
    ListResultSchema,
)
from kit.schema.field import RequiredStr

BannerSchema = class_schema(Banner, base_schema=EntitySchema)


class BannerQueryArgSchema(ListQueryArgSchema):
    code_type = fields.Str(description='自定义类型')
    business_code = fields.Str(description='业务编号')
    name = fields.Str(description='横幅名称')
    status = fields.Int(description='状态(1-显示,0-隐藏)')
    # 排序规则：默认按sort_order排序
    ordering = fields.DelimitedList(fields.Str(), missing=['sort_order'])


class BannerListSchema(ListResultSchema):
    items = fields.List(fields.Nested(BannerSchema()))


class BannerCreateSchema(BannerSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'code_type',
            'business_code',
            'name',
            'upload_image',
            'expand_image',
            'link_type',
            'link_url',
            'remark',
            'status',
            'sort_order',
        )


class BannerUpdateSchema(BannerSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'code_type',
            'business_code',
            'name',
            'upload_image',
            'expand_image',
            'link_type',
            'link_url',
            'remark',
            'status',
            'sort_order',
        )


class BannerStatusSchema(ArgSchema):
    status = fields.Int(required=True, description='状态值(1-显示,0-隐藏)')
