from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.specification import ShopSpecification, ShopSpecificationAttribute
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopSpecificationSchema = class_schema(ShopSpecification, base_schema=EntitySchema)
ShopSpecificationAttributeSchema = class_schema(ShopSpecificationAttribute, base_schema=EntitySchema)


# 规格查询参数 Schema
class ShopSpecificationQueryArgSchema(EntityIntSchema):
    name = webargs_fields.Str(description='规格名称')
    page = webargs_fields.Int(description='页码')
    size = webargs_fields.Int(description='每页条数')


# 规格属性查询参数 Schema
class ShopSpecificationAttributeQueryArgSchema(EntityIntSchema):
    specification_id = webargs_fields.Int(description='规格ID')
    name = webargs_fields.Str(description='属性名称')


# 批量删除参数 Schema
class DeleteIdsSchema(Schema):
    ids = webargs_fields.List(webargs_fields.Int(required=True), required=True, description='要删除的ID列表')


# 响应 Schema
class ReShopSpecificationSchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopSpecificationSchema())
    code = webargs_fields.Int(description='状态码')


class ReShopSpecificationListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopSpecificationSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


class ReShopSpecificationAttributeSchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopSpecificationAttributeSchema())
    code = webargs_fields.Int(description='状态码')


class ReShopSpecificationAttributeListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopSpecificationAttributeSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


# 规格及其属性的组合 Schema
class SpecificationWithAttributesSchema(Schema):
    specification = webargs_fields.Nested(ShopSpecificationSchema())
    attributes = webargs_fields.List(webargs_fields.Nested(ShopSpecificationAttributeSchema()))


class ReSpecificationWithAttributesSchema(EntityIntSchema):
    data = webargs_fields.Nested(SpecificationWithAttributesSchema())
    code = webargs_fields.Int(description='状态码')
