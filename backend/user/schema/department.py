from marshmallow_dataclass import class_schema
from webargs import fields

from backend.user.domain import Department
from kit.schema.base import (
    EntitySchema,
    ListQueryArgSchema,
    ListResultSchema,
)

DepartmentSchema = class_schema(Department, base_schema=EntitySchema)


class DepartmentQueryArgSchema(ListQueryArgSchema):
    ...


class DepartmentListSchema(ListResultSchema):
    items = fields.List(fields.Nested(DepartmentSchema()))


class DepartmentCreateSchema(DepartmentSchema):
    ...


class DepartmentUpdateSchema(DepartmentSchema):
    ...


class DepartmentPatchSchema(DepartmentSchema):
    ...

