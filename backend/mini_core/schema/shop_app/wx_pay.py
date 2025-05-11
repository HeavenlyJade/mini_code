from marshmallow_dataclass import class_schema
from webargs import fields
from marshmallow import Schema, validate
from backend.mini_core.domain.t_user import ShopUser
from kit.schema.base import (
    ArgSchema,
    BaseSchema,
    EntitySchema,
)

from webargs import fields


class WxPay(Schema):
    order_id = fields.Str(description='order_id')

class WxPayData(BaseSchema):
    prepay_id = fields.Str(description='prepay_id')
    appid= fields.Str(description='appid')
    time_stamp =fields.Str(description='timeStamp')
    nonce_str=fields.Str(description='nonceStr')
    package=fields.Str(description='package')
    sign_type=fields.Str(description='signType')
    pay_sign =fields.Str(description='paySign')

class WxPaySchema(Schema):
    data = fields.Nested(WxPayData())
    code = fields.Int(description='code')
    error = fields.Str(description='error')
