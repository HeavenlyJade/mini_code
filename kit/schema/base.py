from typing import Any

from flask_smorest.fields import Upload
from loguru import logger
from marshmallow import EXCLUDE, Schema, ValidationError
from webargs import fields
from webargs import fields as webargs_fields

from kit.exceptions import ServiceBadRequest
from kit.schema.field import DateTime


class BaseSchema(Schema):
    # def handle_error(self, error: ValidationError, data: Any, *, many: bool, **kwargs):
    #     error_map = list(error.messages.values())[0] if many else error.messages
    #     for key, value in error_map.items():
    #         if isinstance(value, dict):
    #             value = list(value.values())[0]
    #         error_msg = f'验证错误, 错误字段为 {key} , 错误为 {";".join(value)}'
    #         logger.info(error_msg)
    #         raise ServiceBadRequest(error_msg)
    def handle_error(self, error, data, **kwargs):
        """Handle ValidationError by raising ServiceBadRequest."""
        error_map = error.messages

        if isinstance(error_map, list):
            # 处理列表错误
            raise ServiceBadRequest(str(error_map))
        elif isinstance(error_map, dict):
            # 处理字典错误
            for key, value in error_map.items():
                if isinstance(value, (list, tuple)):
                    if isinstance(value[0], (dict, list)):
                        raise ServiceBadRequest(f"{key} {str(value)}")
                    raise ServiceBadRequest(f"{key} {value[0]}")
                raise ServiceBadRequest(f"{key} {str(value)}")
        else:
            # 回退处理
            raise ServiceBadRequest(str(error_map))
    class Meta:
        ordered = True


class ArgSchema(BaseSchema):
    class Meta:
        ordered = True
        unknown = EXCLUDE


class EntitySchema(ArgSchema):
    id = fields.Int(dump_only=True)
    create_time = DateTime(dump_only=True, description='创建时间')
    update_time = DateTime(dump_only=True, description='更新时间')


class UuidEntitySchema(EntitySchema):
    id = fields.Str(dump_only=True)


class ListQueryArgSchema(ArgSchema):
    page = fields.Int(description='页码')
    size = fields.Int(description='每页个数')
    need_total_count = fields.Bool(missing=False, description='是否需要统计计数')
    ordering = fields.DelimitedList(fields.Str(), description='排序字段')


class MassArgSchema(ArgSchema):
    record_ids = fields.DelimitedList(
        fields.Int, required=True, description='需要操作的资源ID列表, 以逗号分割'
    )


class RespSchema(Schema):
    ...


class ListResultSchema(BaseSchema):
    total = fields.Int(description='总数')


class UploadArgSchema(ArgSchema):
    file = Upload(
        description='待上传文件', required=True, error_messages={'required': '待上传文件不能为空'}
    )


class EntityIntSchema(ListQueryArgSchema):
    id = fields.Int(dump_only=True)
    create_time = DateTime(dump_only=True, description='创建时间')
    update_time = DateTime(dump_only=True, description='更新时间')
    delete_time = DateTime(dump_only=True, description='删除时间')


class FieldQuerySchema(BaseSchema):
    fields = webargs_fields.List(webargs_fields.Str(), description='入参字段')
