import typing
from functools import partial

from marshmallow.validate import OneOf
from webargs import fields

__all__ = [
    'RequiredStr',
    'AllowNoneStr',
    'Date',
    'DateTime',
    'DateDelimitedList',
    'DateTimeDelimitedList',
    'EnumField',
    'DateTimeStr',
]

from kit.domain.field import ExtendedEnum
from kit.schema import validator


class Date(fields.Date):
    default_error_messages = {'invalid': '日期格式不正确', 'format': '{input}不能被格式化为日期格式'}

    DEFAULT_FORMAT = '%Y-%m-%d'

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        data_format = self.format or self.DEFAULT_FORMAT
        format_func = self.SERIALIZATION_FUNCS.get(data_format)
        if format_func:
            return format_func(value)
        else:
            return value.strftime(data_format)


class DateTime(fields.DateTime):
    default_error_messages = {'invalid': '时间格式不正确', 'format': '{input}不能被格式化为时间格式'}

    DEFAULT_FORMAT = '%Y-%m-%d %H:%M:%S'


class BlankDate(Date):
    def deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str] = None,
        data: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        **kwargs,
    ):
        if value == '':
            value = None
        return super(BlankDate, self).deserialize(value, attr, data, **kwargs)


class BlankDateTime(DateTime):
    def deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str] = None,
        data: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        **kwargs,
    ):
        if value == '':
            value = None
        return super(BlankDateTime, self).deserialize(value, attr, data, **kwargs)


class EnumField:
    def __init__(
        self,
        enum: typing.Type[ExtendedEnum],
        cls_or_instance: typing.Union[
            typing.Type[fields.Int], typing.Type[fields.Str]
        ] = fields.Int,
    ):
        self.enum = enum
        self.cls_or_instance = cls_or_instance

    def fields(self, **kwargs):
        choices = [e.value for e in self.enum]
        error = f'{self.enum.__doc__}必须在{", ".join(map(lambda x: str(x), choices))}之间'
        return partial(
            self.cls_or_instance,
            validate=OneOf(choices=[e.value for e in self.enum], error=error),
            description=self.enum.desc(),
        )(**kwargs)


RequiredStr = partial(fields.Str, required=True)
AllowNoneStr = partial(fields.Str, allow_none=True)
DateDelimitedList = partial(
    fields.DelimitedList, cls_or_instance=BlankDate(allow_none=True)
)
DateTimeDelimitedList = partial(
    fields.DelimitedList, cls_or_instance=BlankDateTime(allow_none=True)
)
DateTimeStr = partial(fields.Str, validate=validator.validate_format_datetime_str)
