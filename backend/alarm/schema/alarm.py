from marshmallow_dataclass import class_schema
from webargs import fields

from backend.alarm.domain import Alarm
from kit.schema.base import EntitySchema, ListQueryArgSchema, ListResultSchema
from kit.schema.field import DateTimeDelimitedList

AlarmSchema = class_schema(Alarm, base_schema=EntitySchema)


class AlarmQueryArgSchema(ListQueryArgSchema):
    eqp_area = fields.Str()
    flow_name = fields.Str()
    alarm_time = DateTimeDelimitedList(description='报警时间')
    # 排序规则：最新的报警数据在前
    ordering = fields.DelimitedList(fields.Str(), missing=['-alarm_time'])


class AlarmListSchema(ListResultSchema):
    items = fields.List(fields.Nested(AlarmSchema()))


class AlarmCreateSchema(AlarmSchema):
    ...
