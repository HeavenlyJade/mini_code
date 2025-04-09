from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.order_detail import OrderDetail
from .order import ShopOrderSchema
from .order_log import OrderLogSchema
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema, ListQueryArgSchema
# 基本 Schema 类 - 使用 class_schema 自动生成
OrderDetailSchema = class_schema(OrderDetail, base_schema=EntitySchema)


# 订单详情查询参数 Schema
class OrderDetailQueryArgSchema(ListQueryArgSchema):
    order_no = webargs_fields.Str(description='订单号')
    sku_id = webargs_fields.Str(description='SKU ID')
    product_id = webargs_fields.Int(description='商品ID')
    product_name = webargs_fields.Str(description='商品名称')
    refund_status = webargs_fields.Int(description='退款状态,0:无退款,1退款中,2，已拒绝,3，已完成')
    is_gift = webargs_fields.Int(description='是否赠品', validate=validate.OneOf([0, 1]))


# 订单详情创建参数 Schema
class OrderDetailCreateSchema(Schema):
    order_no = webargs_fields.Str(required=True, description='订单号')
    sku_id = webargs_fields.Str(required=True, description='SKU ID')
    product_id = webargs_fields.Int(required=True, description='商品ID')
    sku_code = webargs_fields.Str(required=True, description='SKU编码')
    price = webargs_fields.Decimal(required=True, description='原价格')
    actual_price = webargs_fields.Decimal(required=True, description='实际购买价格')
    num = webargs_fields.Int(required=True, description='购买数量')
    product_img = webargs_fields.Str(description='商品图片')
    product_spec = webargs_fields.Str(description='商品规格')
    product_name = webargs_fields.Str(required=True, description='商品名称')
    quantity = webargs_fields.Int(description='商品数量')
    unit_price = webargs_fields.Decimal(description='商品单价')
    total_price = webargs_fields.Decimal(description='商品总价')
    is_gift = webargs_fields.Int(description='是否赠品', validate=validate.OneOf([0, 1]), missing=0)
    refund_status = webargs_fields.Int(description="退款状态",validate=validate.OneOf(["无退款", "退款中", "已完成", "已驳回"]))


# 批量创建订单详情 Schema
class BatchCreateOrderDetailSchema(Schema):
    items = webargs_fields.List(webargs_fields.Nested(OrderDetailCreateSchema), required=True)


# 响应 Schema
class OrderDetailResponseSchema(EntityIntSchema):
    data = webargs_fields.Nested(OrderDetailSchema())
    code = webargs_fields.Int(description='状态码')


class OrderDetailListResponseSchema(ListResultSchema):
    order_details = webargs_fields.List(webargs_fields.Nested(OrderDetailSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')
