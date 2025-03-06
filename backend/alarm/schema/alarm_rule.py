from marshmallow_dataclass import class_schema

from backend.alarm.domain import AlarmRule
from kit.schema.base import EntitySchema

AlarmRuleSchema = class_schema(AlarmRule, base_schema=EntitySchema)


class AlarmRuleUpdateSchema(AlarmRuleSchema):
    ...
