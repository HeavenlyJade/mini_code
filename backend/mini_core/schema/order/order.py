from marshmallow_dataclass import class_schema
from marshmallow import Schema, fields
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.order import ShopOrder
from kit.schema.base import EntitySchema, ListResultSchema, ListQueryArgSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopOrderSchema = class_schema(ShopOrder, base_schema=EntitySchema)


# 订单查询参数 Schema
class ShopOrderQueryArgSchema(ListQueryArgSchema):
    order_no = webargs_fields.Str(description='订单编号')
    order_sn = webargs_fields.Str(description='订单号')
    user_id = webargs_fields.Int(description='用户ID')
    nickname = webargs_fields.Str(description='用户昵称')
    phone = webargs_fields.Str(description='用户手机号')
    order_type = webargs_fields.Str(description='订单类型')
    order_source = webargs_fields.Str(description='订单来源')
    status = webargs_fields.Str(description='订单状态')
    payment_status = webargs_fields.Str(description='支付状态')
    delivery_status = webargs_fields.Str(description='配送状态')
    refund_status = webargs_fields.Str(description='退款状态')
    product_id = webargs_fields.Int(description='商品ID')
    sku_id = webargs_fields.Int(description='SKU ID')
    receiver_name = webargs_fields.Str(description='收货人姓名')
    receiver_phone = webargs_fields.Str(description='收货人电话')
    express_no = webargs_fields.Str(description='快递单号')
    start_time = webargs_fields.DateTime(description='开始时间')
    end_time = webargs_fields.DateTime(description='结束时间')
    payment_start_time = webargs_fields.DateTime(description='支付开始时间')
    payment_end_time = webargs_fields.DateTime(description='支付结束时间')
    ship_start_time = webargs_fields.DateTime(description='发货开始时间')
    ship_end_time = webargs_fields.DateTime(description='发货结束时间')
    min_amount = webargs_fields.Float(description='最小金额')
    max_amount = webargs_fields.Float(description='最大金额')
    keyword = webargs_fields.Str(description='关键词搜索')


# 订单状态更新参数 Schema
class OrderStatusUpdateArgSchema(Schema):
    order_no = webargs_fields.Str(required=True, description='订单ID')
    status = webargs_fields.Str(description='订单状态')


# 支付状态更新参数 Schema
class PaymentStatusUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='订单ID')
    payment_status = webargs_fields.Str(required=True, description='支付状态')
    payment_no = webargs_fields.Str(description='支付单号')
    trade_no = webargs_fields.Str(description='交易号')


# 配送状态更新参数 Schema
class DeliveryStatusUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='订单ID')
    delivery_status = webargs_fields.Str(required=True, description='配送状态')
    express_company = webargs_fields.Str(description='快递公司')
    express_no = webargs_fields.Str(description='快递单号')
    delivery_platform = webargs_fields.Str(description='配送平台')




# 订单创建参数 Schema
class OrderCreateSchema(Schema):
    user_id = webargs_fields.Int(required=True, description='用户ID')
    nickname = webargs_fields.Str(description='用户昵称')
    phone = webargs_fields.Str(description='用户手机号')
    order_type = webargs_fields.Str(required=True, description='订单类型')
    order_source = webargs_fields.Str(description='订单来源')
    product_id = webargs_fields.Int(required=True, description='商品ID')
    product_name = webargs_fields.Str(required=True, description='商品名称')
    sku_id = webargs_fields.Int(description='SKU ID')
    sku_code = webargs_fields.Str(description='SKU编码')
    product_img = webargs_fields.Str(description='商品图片')
    product_spec = webargs_fields.Str(description='商品规格')
    quantity = webargs_fields.Int(required=True, description='商品数量')
    unit_price = webargs_fields.Float(required=True, description='商品单价')
    total_price = webargs_fields.Float(required=True, description='商品总价')
    is_gift = webargs_fields.Bool(description='是否赠品')
    receiver_name = webargs_fields.Str(required=True, description='收货人姓名')
    receiver_phone = webargs_fields.Str(required=True, description='收货人电话')
    province = webargs_fields.Str(required=True, description='省份')
    city = webargs_fields.Str(required=True, description='城市')
    district = webargs_fields.Str(required=True, description='区/县')
    address = webargs_fields.Str(required=True, description='详细地址')
    postal_code = webargs_fields.Str(description='邮编')
    id_card_no = webargs_fields.Str(description='身份证号码')
    remark = webargs_fields.Str(description='备注')
    client_remark = webargs_fields.Str(description='客户备注')
    pre_sale_time = webargs_fields.DateTime(description='预售日期')


# 日期范围查询参数 Schema
class DateRangeQueryArgSchema(Schema):
    start_date = webargs_fields.DateTime(description='开始日期')
    end_date = webargs_fields.DateTime(description='结束日期')


# 订单统计信息 Schema
class OrderSourceStatsSchema(Schema):
    source = webargs_fields.Str(description='订单来源')
    count = webargs_fields.Int(description='数量')


class OrderTypeStatsSchema(Schema):
    type = webargs_fields.Str(description='订单类型')
    count = webargs_fields.Int(description='数量')


class OrderStatsSchema(Schema):
    total = webargs_fields.Int(description='总订单数')
    pending_payment = webargs_fields.Int(description='待支付订单数')
    pending_delivery = webargs_fields.Int(description='待发货订单数')
    delivering = webargs_fields.Int(description='配送中订单数')
    completed = webargs_fields.Int(description='已完成订单数')
    cancelled = webargs_fields.Int(description='已取消订单数')
    today_orders = webargs_fields.Int(description='今日订单数')
    today_sales = webargs_fields.Float(description='今日销售额')
    source_stats = webargs_fields.List(webargs_fields.Nested(OrderSourceStatsSchema()), description='来源统计')
    type_stats = webargs_fields.List(webargs_fields.Nested(OrderTypeStatsSchema()), description='类型统计')


# 月度销售统计 Schema
class MonthlySalesSchema(Schema):
    month = webargs_fields.Str(description='月份')
    order_count = webargs_fields.Int(description='订单数')
    total_sales = webargs_fields.Float(description='销售额')


# 响应 Schema
class ReShopOrderSchema(Schema):
    data = webargs_fields.Nested(ShopOrderSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='错误信息')
    total = webargs_fields.Int(description='数量')


class ReShopOrderListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopOrderSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


class ReOrderStatsSchema(Schema):
    data = webargs_fields.Nested(OrderStatsSchema())
    code = webargs_fields.Int(description='状态码')


class ReMonthlySalesSchema(Schema):
    data = webargs_fields.List(webargs_fields.Nested(MonthlySalesSchema()))
    code = webargs_fields.Int(description='状态码')


class GoodsItemSchema(Schema):
    """Schema for individual goods items in the order"""
    product_id = fields.Int(required=True)
    number = fields.Int(required=True)
    price = fields.Decimal(required=True)
    cart_id = fields.Int(required=True)


class MiniOrderCreateSchema(Schema):
    """Schema for mini program order creation"""
    final_amount = fields.Decimal(required=True, description='订单总金额')
    member_level = fields.Str(required=True, description='等级的id字段')
    original_amount = fields.Decimal(required=True, description='折扣前金额')
    member_discount = fields.Decimal(required=True, description='会员折扣金额')
    benefit = fields.Decimal(required=True, description='优惠金额')
    points_deduct_amount =  fields.Decimal( description='积分抵扣金额')
    points_used = fields.Int(description='积分的抵扣金额')
    postage = fields.Decimal(required=True, description='邮费')
    address = fields.Str(required=True, description='地址信息JSON字符串')
    goodsDetail = fields.Str(required=True, description='商品详情JSON字符串')
    memo = fields.Str(description='备注')
    userDetail = fields.Str(required=True, description='用户信息JSON字符串')
    userId = fields.Int(required=True, description='用户ID')
    timestamp = fields.Int(required=True, description='时间戳')
    signStr = fields.Str(required=True, description='签名')


class WXShopOrderQueryArgSchema(ListQueryArgSchema):
    user_id = webargs_fields.Int(description='用户ID')
    status = webargs_fields.Str(description='订单状态')
    refund_reason = webargs_fields.Str(description='退款理由')

# 物流信息更新参数 Schema
class ShippingInfoUpdateArgSchema(Schema):
    order_no = webargs_fields.Str(required=True, description='订单编号')
    express_company = webargs_fields.Str(description='快递公司名称')
    express_no = webargs_fields.Str(description='快递单号')
    delivery_platform = webargs_fields.Str(description='配送平台')
    remark = webargs_fields.Str(description='备注')
