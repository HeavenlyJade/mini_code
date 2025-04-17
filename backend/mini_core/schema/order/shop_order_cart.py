from marshmallow import Schema, validate
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.shop_order_cart import ShopOrderCart
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema, ListQueryArgSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopOrderCartSchema = class_schema(ShopOrderCart, base_schema=EntitySchema)


# 购物车查询参数 Schema
class ShopOrderCartQueryArgSchema(ListQueryArgSchema):
    user_id = webargs_fields.Str(description='用户ID')
    open_id = webargs_fields.Str(description='微信openID')
    sku_id = webargs_fields.Int(description='商品SKU ID')


# 购物车商品添加参数 Schema
class CartItemAddSchema(Schema):
    sku_id = webargs_fields.Int(required=True, description='商品SKU ID')
    product_count = webargs_fields.Int(required=True, description='商品数量', validate=validate.Range(min=1))


# 购物车商品更新参数 Schema
class CartItemUpdateSchema(Schema):
    id = webargs_fields.Int(required=True, description='购物车项ID')
    sku_id = webargs_fields.Int(required=True, description='商品id')

    product_count = webargs_fields.Int(required=True, description='商品数量', validate=validate.Range(min=1))


# 购物车商品删除参数 Schema
class CartItemDeleteSchema(Schema):
    sku_id = webargs_fields.Int(required=True, description='商品SKU ID')


# 商品详细信息 Schema (包含产品详情)
class CartItemProductDetailSchema(Schema):
    cart_item = webargs_fields.Nested(ShopOrderCartSchema())
    product_name = webargs_fields.Str(description='商品名称')
    product_image = webargs_fields.Str(description='商品图片')
    price = webargs_fields.Decimal(description='商品价格')
    original_price = webargs_fields.Decimal(description='原价')
    stock = webargs_fields.Int(description='库存')
    spec_text = webargs_fields.Str(description='规格文本')


# 响应 Schema
class ShopOrderCartResponseSchema(Schema):
    data = webargs_fields.Nested(ShopOrderCartSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class ShopOrderCartListResponseSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopOrderCartSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


class CartItemWithProductListResponseSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(CartItemProductDetailSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')
    total_count = webargs_fields.Int(description='商品总数')
    total_price = webargs_fields.Decimal(description='总价')
