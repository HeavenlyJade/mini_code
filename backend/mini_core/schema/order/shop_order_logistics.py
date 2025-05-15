from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.shop_order_logistics import ShopOrderLogistics
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema, ListQueryArgSchema
from kit.schema.field import DateTimeDelimitedList

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopOrderLogisticsSchema = class_schema(ShopOrderLogistics, base_schema=EntitySchema)


# 物流查询参数 Schema
class ShopOrderLogisticsQueryArgSchema(ListQueryArgSchema):
    order_no = webargs_fields.Str(description='订单编号')
    logistics_no = webargs_fields.Str(description='物流单号')
    logistics_company = webargs_fields.Str(description='物流公司')
    courier_number = webargs_fields.Str(description='快递员编号')
    courier_phone = webargs_fields.Str(description='快递员电话')
    current_status = webargs_fields.Str(description='当前状态')
    current_location = webargs_fields.Str(description='当前位置')
    shipping_time = DateTimeDelimitedList(description='发货时间范围')
    shipping_start_time = webargs_fields.DateTime(description='发货开始时间')
    shipping_end_time = webargs_fields.DateTime(description='发货结束时间')
    estimate_time = DateTimeDelimitedList(description='预计送达时间范围')
    estimate_start_time = webargs_fields.DateTime(description='预计送达开始时间')
    estimate_end_time = webargs_fields.DateTime(description='预计送达结束时间')
    receiving_time = DateTimeDelimitedList(description='实际收货时间范围')
    receiving_start_time = webargs_fields.DateTime(description='实际收货开始时间')
    receiving_end_time = webargs_fields.DateTime(description='实际收货结束时间')
    start_date = DateTimeDelimitedList(description='记录开始时间范围')
    end_date = DateTimeDelimitedList(description='记录结束时间范围')
    ordering = webargs_fields.DelimitedList(webargs_fields.Str(), missing=['-create_time'])


# 地址信息 Schema
class AddressInfoSchema(Schema):
    name = webargs_fields.Str(required=True, description='姓名')
    phone = webargs_fields.Str(required=True, description='电话')
    province = webargs_fields.Str(required=True, description='省份')
    city = webargs_fields.Str(required=True, description='城市')
    district = webargs_fields.Str(required=True, description='区/县')
    address = webargs_fields.Str(required=True, description='详细地址')
    postal_code = webargs_fields.Str(description='邮政编码')


# 物流轨迹项 Schema
class LogisticsTrackItemSchema(Schema):
    time = webargs_fields.Str( description='时间')  # Change from DateTime to Str
    status = webargs_fields.Str(description='状态')
    location = webargs_fields.Str(description='位置')
    remark = webargs_fields.Str(description='备注')


# 物流创建参数 Schema
class ShopOrderLogisticsCreateSchema(Schema):
    order_no = webargs_fields.Str(required=True, description='订单编号')
    logistics_no = webargs_fields.Str(required=True, description='物流单号')
    logistics_company = webargs_fields.Str(required=True, description='物流公司')
    courier_number = webargs_fields.Str(description='快递员编号')
    courier_phone = webargs_fields.Str(description='快递员电话')
    sender_info = webargs_fields.Str(description='发件人信息(JSON格式)')
    receiver_info = webargs_fields.Str(required=True, description='收件人信息(JSON格式)')
    shipping_time = webargs_fields.DateTime(description='发货时间')
    estimate_time = webargs_fields.DateTime(description='预计送达时间')
    current_status = webargs_fields.Str(required=True, description='当前状态')
    current_location = webargs_fields.Str(description='当前位置')
    logistics_route = webargs_fields.Str(description='物流轨迹(JSON格式)')
    remark = webargs_fields.Str(description='备注')


# 物流更新参数 Schema
class ShopOrderLogisticsUpdateSchema(Schema):
    logistics_company = webargs_fields.Str(description='物流公司')
    logistics_no = webargs_fields.Str(description='物流单号')
    courier_number = webargs_fields.Str(description='快递员编号')
    courier_phone = webargs_fields.Str(description='快递员电话')
    sender_info = webargs_fields.Str(description='发件人信息(JSON格式)')
    receiver_info = webargs_fields.Str(description='收件人信息(JSON格式)')
    shipping_time = webargs_fields.DateTime(description='发货时间')
    estimate_time = webargs_fields.DateTime(description='预计送达时间')
    receiving_time = webargs_fields.DateTime(description='实际收货时间')
    current_status = webargs_fields.Str(description='当前状态')
    current_location = webargs_fields.Str(description='当前位置')
    remark = webargs_fields.Str(description='备注')


# 物流状态更新参数 Schema
class LogisticsStatusUpdateSchema(Schema):
    status = webargs_fields.Str(required=True, description='物流状态')
    location = webargs_fields.Str(description='当前位置')
    remark = webargs_fields.Str(description='备注')


# 物流发货参数 Schema
class LogisticsShipSchema(Schema):
    shipping_time = webargs_fields.DateTime(description='发货时间')
    estimate_time = webargs_fields.DateTime(description='预计送达时间')
    logistics_company = webargs_fields.Str(required=True, description='物流公司')
    logistics_no = webargs_fields.Str(required=True, description='物流单号')
    courier_number = webargs_fields.Str(description='快递员编号')
    courier_phone = webargs_fields.Str(description='快递员电话')
    current_location = webargs_fields.Str(description='发货位置')
    remark = webargs_fields.Str(description='备注')


# 物流送达参数 Schema
class LogisticsDeliveredSchema(Schema):
    receiving_time = webargs_fields.DateTime(description='实际收货时间')
    remark = webargs_fields.Str(description='备注')


# 物流日期范围查询参数 Schema
class LogisticsDateRangeQueryArgSchema(Schema):
    start_date = webargs_fields.DateTime(required=True, description='开始日期')
    end_date = webargs_fields.DateTime(required=True, description='结束日期')


# 响应 Schema
class ShopOrderLogisticsResponseSchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopOrderLogisticsSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class ShopOrderLogisticsListResponseSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopOrderLogisticsSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


# 物流详细信息响应 Schema（包含解析后的JSON字段）
class LogisticsDetailSchema(Schema):
    id = webargs_fields.Int(description='ID')
    order_no = webargs_fields.Str(description='订单编号')
    logistics_no = webargs_fields.Str(description='物流单号')
    logistics_company = webargs_fields.Str(description='物流公司')
    courier_number = webargs_fields.Str(description='快递员编号')
    courier_phone = webargs_fields.Str(description='快递员电话')
    sender_info = webargs_fields.Nested(AddressInfoSchema, description='发件人信息')
    receiver_info = webargs_fields.Nested(AddressInfoSchema, description='收件人信息')
    shipping_time = webargs_fields.DateTime(description='发货时间')
    estimate_time = webargs_fields.DateTime(description='预计送达时间')
    receiving_time = webargs_fields.DateTime(description='实际收货时间')
    current_status = webargs_fields.Str(description='当前状态')
    current_location = webargs_fields.Str(description='当前位置')
    logistics_route = webargs_fields.List(webargs_fields.Nested(LogisticsTrackItemSchema), description='物流轨迹')
    remark = webargs_fields.Str(description='备注')
    start_date = webargs_fields.DateTime(description='记录开始时间')
    end_date = webargs_fields.DateTime(description='记录结束时间')
    create_time = webargs_fields.DateTime(description='创建时间')
    update_time = webargs_fields.DateTime(description='更新时间')


class LogisticsDetailResponseSchema(Schema):
    data = webargs_fields.Nested(LogisticsDetailSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


# 物流状态统计响应 Schema
class LogisticsStatusCountSchema(Schema):
    status = webargs_fields.Str(description='物流状态')
    count = webargs_fields.Int(description='数量')


class LogisticsStatsResponseSchema(Schema):
    total = webargs_fields.Int(description='总数')
    active = webargs_fields.Int(description='活跃数量')
    delivered = webargs_fields.Int(description='已送达数量')
    status_stats = webargs_fields.List(webargs_fields.Nested(LogisticsStatusCountSchema), description='状态统计')
    code = webargs_fields.Int(description='状态码')


class LogisticsQuerySchema(Schema):
    order_no =  webargs_fields.Str(description='订单号')
