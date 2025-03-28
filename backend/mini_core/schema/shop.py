from marshmallow import validate, Schema, validates, ValidationError
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.shop import ShopProduct, ShopProductCategory
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ProductCategorySchema = class_schema(ShopProductCategory, base_schema=EntitySchema)
ShopProductSchema = class_schema(ShopProduct, base_schema=EntitySchema)


# 分类查询参数 Schema
class ProductCategoryQueryArgSchema(EntityIntSchema):
    name = webargs_fields.Str(description='分类名称')
    code = webargs_fields.Str(description='编号')
    parent_id = webargs_fields.Int(description='上级分类ID')
    type = webargs_fields.Str(description='类型')
    status = webargs_fields.Str(description='状态')


# 商品查询参数 Schema
class ShopProductQueryArgSchema(EntityIntSchema):
    name = webargs_fields.Str(description='商品名称')
    code = webargs_fields.Str(description='商品编号')
    category_id = webargs_fields.Int(description='商品分类ID')
    status = webargs_fields.Str(description='状态')
    type = webargs_fields.Str(description='类型')
    is_recommended = webargs_fields.Bool(description='是否推荐')
    price_min = webargs_fields.Decimal(description='最低价格')
    price_max = webargs_fields.Decimal(description='最高价格')
    keyword = webargs_fields.Str(description='关键词')


# 商品库存更新参数 Schema
class ShopProductStockUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商品ID')
    quantity = webargs_fields.Int(required=True, description='变更数量，可以是正数或负数')

    @validates("quantity")
    def validate_quantity(self, value):
        if value == 0:
            raise ValidationError("变更数量不能为0")


# 商品状态更新参数 Schema
class ShopProductStatusUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商品ID')
    status = webargs_fields.Str(required=True, description='商品状态：上架 或 下架',
                                validate=validate.OneOf(["上架", "下架"]))
class ReProductCategorySchema(EntityIntSchema):
    data = webargs_fields.Nested(ProductCategorySchema())
    code = webargs_fields.Int(description='状态')

class ReProductCategoryListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ProductCategorySchema()))
    code = webargs_fields.Int(description='状态')
    total = webargs_fields.Int(description='总数')


class ReShopProductSchema(Schema):
    data = webargs_fields.Nested(ShopProductSchema())
    code = webargs_fields.Int(description='状态')


class ReShopProductListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopProductSchema()))
    code = webargs_fields.Int(description='状态')


# 商品分类树节点 Schema
class ProductCategoryTreeNodeSchema(Schema):
    id = webargs_fields.Int(description='分类ID')
    name = webargs_fields.Str(description='分类名称')
    code = webargs_fields.Str(description='编号')
    children = webargs_fields.List(webargs_fields.Nested(lambda: ProductCategoryTreeNodeSchema()), description='子分类')


# 分类树响应 Schema
class ReProductCategoryTreeSchema(EntityIntSchema):
    data = webargs_fields.List(webargs_fields.Nested(ProductCategoryTreeNodeSchema()))
    code = webargs_fields.Int(description='状态')


# 商品库存更新响应 Schema
class ReShopProductStockUpdateSchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopProductSchema())
    stock_warning = webargs_fields.Bool(description='库存是否低于预警值')
    code = webargs_fields.Int(description='状态')
