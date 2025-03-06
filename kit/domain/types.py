import datetime as dt

from marshmallow import validate
from marshmallow_dataclass import NewType

from kit.schema.field import DateTime

__all__ = ['StrField', 'DateTimeField']

StrField = NewType('Str', str, validate=validate.Length(max=255))
DateTimeField = NewType('DateTime', dt.datetime, field=DateTime)
