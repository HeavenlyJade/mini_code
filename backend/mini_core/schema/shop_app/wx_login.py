from marshmallow_dataclass import class_schema
from webargs import fields

from backend.mini_core.domain.t_user import ShopUser
from kit.schema.base import (
    ArgSchema,
    BaseSchema,
    EntitySchema,
)

ShopUserSchema = class_schema(ShopUser, base_schema=EntitySchema)


class WechatLoginSchema(ArgSchema):
    code = fields.Str(required=True, description='微信临时登录凭证')
    nickName = fields.Str(required=True, description='微信用户')
    avatarUrl = fields.Str(required=True, description='用户图片')


class ShopAppSchema(BaseSchema):
    user_info = fields.Nested(ShopUserSchema())
    access_token = fields.Str()
    refresh_token = fields.Str()
    msg = fields.Str()
    code = fields.Int()
