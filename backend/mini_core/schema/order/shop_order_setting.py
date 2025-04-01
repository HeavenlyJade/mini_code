from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.shop_order_setting import ShopOrderSetting
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopOrderSettingSchema = class_schema(ShopOrderSetting, base_schema=EntitySchema)


# 订单配置查询参数 Schema
class ShopOrderSettingQueryArgSchema(EntityIntSchema):
    shop_id = webargs_fields.Int(description='店铺ID')


# 店铺订单配置相关参数校验 Schema
class ValidateShopOrderSettingSchema(Schema):
    auto_close_minutes = webargs_fields.Int(
        validate=validate.Range(min=1, max=1440),
        description='自动关闭时间(分钟, 1-1440)'
    )
    auto_receive_days = webargs_fields.Int(
        validate=validate.Range(min=1, max=30),
        description='自动收货时间(天, 1-30)'
    )
    logistics_timeout_hours = webargs_fields.Int(
        validate=validate.Range(min=0, max=72),
        description='物流超时提醒时间(小时, 0-72, 0表示不提醒)'
    )
    points_rate = webargs_fields.Decimal(
        validate=validate.Range(min=0),
        description='积分抵扣比例(1元等于多少积分, >=0)'
    )


# 响应 Schema
class ReShopOrderSettingSchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopOrderSettingSchema())
    code = webargs_fields.Int(description='状态码')


class ReShopOrderSettingListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopOrderSettingSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')
