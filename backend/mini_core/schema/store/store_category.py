from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.store import ShopStoreCategory
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopStoreCategorySchema = class_schema(ShopStoreCategory, base_schema=EntitySchema)


# 分类查询参数 Schema
class ShopStoreCategoryQueryArgSchema(EntityIntSchema):
    name = webargs_fields.Str(description='分类名称')
    code = webargs_fields.Str(description='编号')
    parent_id = webargs_fields.Int(description='上级分类ID')
    status = webargs_fields.Str(description='状态')
    is_recommend = webargs_fields.Bool(description='是否推荐')


# 分类状态更新参数 Schema
class ShopStoreCategoryStatusUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='分类ID')
    status = webargs_fields.Str(required=True, description='分类状态：正常 或 停用',
                               validate=validate.OneOf(["正常", "停用"]))


class ReShopStoreCategorySchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopStoreCategorySchema())
    code = webargs_fields.Int(description='状态码')


class ReShopStoreCategoryListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopStoreCategorySchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


# 分类树节点 Schema
class ShopStoreCategoryTreeNodeSchema(Schema):
    id = webargs_fields.Int(description='分类ID')
    name = webargs_fields.Str(description='分类名称')
    code = webargs_fields.Str(description='编号')
    sort_order = webargs_fields.Int(description='排序')
    status = webargs_fields.Str(description='状态')
    is_recommend = webargs_fields.Bool(description='是否推荐')
    children = webargs_fields.List(webargs_fields.Nested(lambda: ShopStoreCategoryTreeNodeSchema()), description='子分类')


# 分类树响应 Schema
class ReShopStoreCategoryTreeSchema(EntityIntSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopStoreCategoryTreeNodeSchema()))
    code = webargs_fields.Int(description='状态码')
