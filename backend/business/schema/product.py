from marshmallow_dataclass import class_schema
from webargs import fields

from backend.business.domain.product import Product
from kit.schema.base import EntitySchema, ListQueryArgSchema, ListResultSchema

ProductSchema = class_schema(Product, base_schema=EntitySchema)


class ProductQueryArgSchema(ListQueryArgSchema):
    ...


class ProductListSchema(ListResultSchema):
    items = fields.List(fields.Nested(ProductSchema()))
