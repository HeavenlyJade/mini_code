from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.card import Card
from kit.schema.base import EntitySchema, ListQueryArgSchema, ListResultSchema

CardSchema = class_schema(Card, base_schema=EntitySchema)


class CardQueryArgSchema(EntitySchema):
    openid = webargs_fields.Str(description='微信openID')
    id = webargs_fields.Int(description='名片ID')


class CardUserSchema(ListQueryArgSchema):
    name = webargs_fields.Str(description='用户名')
    openid = webargs_fields.Str(description='微信ID')
    weixing = webargs_fields.Str(description='微信')
    position = webargs_fields.Str(description='职位')
    company = webargs_fields.Str(description='公司')
    phone = webargs_fields.Int(description='电话')


class ReCardSchema(EntitySchema):
    data = webargs_fields.Nested(CardSchema())
    code = webargs_fields.Int(description='状态')
    message = webargs_fields.Str(description='返回消息', required=False)


class ReCardSchemaList(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(CardSchema()))
    code = webargs_fields.Int(description='状态')
    total = webargs_fields.Int(description='总数')
