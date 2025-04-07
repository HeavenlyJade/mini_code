from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.store import ShopStore
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema,ListQueryArgSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
ShopStoreSchema = class_schema(ShopStore, base_schema=EntitySchema)


# 商店查询参数 Schema
class ShopStoreQueryArgSchema(ListQueryArgSchema):
    name = webargs_fields.Str(description='商店名称')
    type = webargs_fields.Str(description='商店类型')
    store_code = webargs_fields.Str(description='门店编号')
    category_id = webargs_fields.Int(description='门店分类ID')
    province = webargs_fields.Str(description='省市区')
    status = webargs_fields.Str(description='状态')
    keyword = webargs_fields.Str(description='关键词')
    min_service_fee_rate = webargs_fields.Float(description='最低服务费率')
    max_service_fee_rate = webargs_fields.Float(description='最高服务费率')
    min_delivery_price = webargs_fields.Float(description='最低配送价格')
    max_delivery_price = webargs_fields.Decimal(description='最高配送价格')


# 商店状态更新参数 Schema
class ShopStoreStatusUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商店ID')
    status = webargs_fields.Str(required=True, description='商店状态：正常 或 停用',
                              validate=validate.OneOf(["正常", "停用"]))


# 附近商店查询参数 Schema
class NearbyStoreQueryArgSchema(Schema):
    latitude = webargs_fields.Float(required=True, description='纬度')
    longitude = webargs_fields.Float(required=True, description='经度')
    distance = webargs_fields.Float(description='距离范围（公里）', missing=5.0)


# 服务模式切换参数 Schema
class ServiceModeToggleArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商店ID')
    mode_type = webargs_fields.Str(required=True, description='模式类型',
                                 validate=validate.OneOf(["takeout_enabled", "self_pickup_enabled", "dine_in_enabled"]))
    enabled = webargs_fields.Bool(required=True, description='是否启用')


# 商店营业时间更新参数 Schema
class BusinessHoursUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商店ID')
    opening_hours = webargs_fields.Str(required=True, description='营业时间')


# 商店配送设置更新参数 Schema
class DeliverySettingsUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商店ID')
    delivery_price = webargs_fields.Float(required=True, description='配送价格')
    min_order_amount = webargs_fields.Float(required=True, description='最小订单金额')


# 商店联系信息更新参数 Schema
class ContactInfoUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商店ID')
    contact_person = webargs_fields.Str(required=True, description='联系人')
    contact_phone = webargs_fields.Str(required=True, description='联系电话')


# 商店WiFi设置更新参数 Schema
class WifiSettingsUpdateArgSchema(Schema):
    id = webargs_fields.Int(required=True, description='商店ID')
    wifi_name = webargs_fields.Str(required=True, description='WiFi名称')
    wifi_password = webargs_fields.Str(required=True, description='WiFi密码')


# 响应 Schema
class ReShopStoreSchema(Schema):
    data = webargs_fields.Nested(ShopStoreSchema())
    code = webargs_fields.Int(description='状态码')


class ReShopStoreListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(ShopStoreSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


# 商店统计信息 Schema
class StoreTypeStatsSchema(Schema):
    type = webargs_fields.Str(description='商店类型')
    count = webargs_fields.Int(description='数量')


class StoreProvinceStatsSchema(Schema):
    province = webargs_fields.Str(description='省市区')
    count = webargs_fields.Int(description='数量')


class ShopStoreStatsSchema(Schema):
    total = webargs_fields.Int(description='总数')
    active = webargs_fields.Int(description='正常状态数量')
    inactive = webargs_fields.Int(description='停用状态数量')
    type_stats = webargs_fields.List(webargs_fields.Nested(StoreTypeStatsSchema()), description='类型统计')
    province_stats = webargs_fields.List(webargs_fields.Nested(StoreProvinceStatsSchema()), description='省份统计')


class ReShopStoreStatsSchema(EntityIntSchema):
    data = webargs_fields.Nested(ShopStoreStatsSchema())
    code = webargs_fields.Int(description='状态码')


# 附近商店响应 Schema
class NearbyStoreSchema(ShopStoreSchema):
    distance = webargs_fields.Decimal(description='距离（公里）')


class ReNearbyStoreListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(NearbyStoreSchema()))
    code = webargs_fields.Int(description='状态码')

class KeywordSearchSchema(Schema):
    keyword = webargs_fields.Str(required=True, description='搜索关键词')


