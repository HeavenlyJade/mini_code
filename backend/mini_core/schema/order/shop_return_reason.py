from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.shop_return_reason import ShopReturnReason
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopReturnReasonSchema = class_schema(ShopReturnReason, base_schema=EntitySchema)


# 退货原因查询参数 Schema
class ShopReturnReasonQueryArgSchema(EntityIntSchema):
    reason_type = webargs_fields.Str(description='原因类型')
    is_enabled = webargs_fields.Bool(description='是否可用')
    page = webargs_fields.Int(description='页码')
    size = webargs_fields.Int(description='每页条数')


# 退货原因状态更新参数 Schema
class ReturnReasonStatusUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='退货原因ID')
    is_enabled = webargs_fields.Bool(required=True, description='是否启用')


# 退货原因排序更新参数 Schema
class ReturnReasonSortUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='退货原因ID')
    sort_order = webargs_fields.Int(required=True, description='排序值', validate=validate.Range(min=1))


# 批量删除参数 Schema
class DeleteIdsSchema(Schema):
    ids = webargs_fields.List(webargs_fields.Int(required=True), required=True, description='要删除的ID列表')


# 响应 Schema
class ReShopReturnReasonSchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopReturnReasonSchema())
    code = webargs_fields.Int(description='状态码')


class ReShopReturnReasonListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopReturnReasonSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')
