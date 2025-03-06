from marshmallow_dataclass import class_schema
from webargs import fields

from backend.log.domain.log import Log, LogOperatingType
from kit.schema.base import EntitySchema, ListQueryArgSchema, ListResultSchema
from kit.schema.field import DateTimeDelimitedList, EnumField

LogSchema = class_schema(Log, base_schema=EntitySchema)


class LogQueryArgSchema(ListQueryArgSchema):
    operating_user = fields.Str(description='操作用户')
    operating_type = EnumField(LogOperatingType).fields()
    operating_time = DateTimeDelimitedList()
    # 排序规则：最新创建的数据在前
    ordering = fields.DelimitedList(fields.Str(), missing=['-create_time'])


class LogListSchema(ListResultSchema):
    items = fields.List(fields.Nested(LogSchema()))


class LogCreateSchema(LogSchema):
    ...
