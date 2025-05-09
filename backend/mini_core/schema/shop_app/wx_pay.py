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
    oder_id = fields.Str(description='oder_id')

class WxPaySchema(Schema):
    prepay_id = fields.Str(description='prepay_id')
    code = fields.Int(description='code')
    error = fields.Str(description='error')
