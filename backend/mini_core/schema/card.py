from marshmallow_dataclass import class_schema
from webargs import fields

from backend.mini_core.domain.card import Card
from kit.schema.base import EntitySchema, ListQueryArgSchema, ListResultSchema

CardSchema = class_schema(Card, base_schema=EntitySchema)


class CardQueryArgSchema(EntitySchema):
    openid = fields.Str(description='部门')

class CardUserSchema(EntitySchema):
    name = fields.Str(description='用户名')
    openid = fields.Str(description='微信iD')
    weixing = fields.Str(description='微信')
    position = fields.Str(description='职位  ')
    company = fields.Str(description='公司')
    phone= fields.Int(description='电话')


class ReCardSchema(EntitySchema):
    data = fields.Nested(CardUserSchema())
    code = fields.Int(description='状态')
