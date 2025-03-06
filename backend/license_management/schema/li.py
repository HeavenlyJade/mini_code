# -*- coding: utf-8 -*-
# author zyy
from marshmallow_dataclass import class_schema
from webargs import fields

from backend.license_management.domain.li import License
from kit.schema.base import EntitySchema, ArgSchema, BaseSchema

LiSchema = class_schema(License, base_schema=EntitySchema)


class LiQueryArgSchemaRequests(ArgSchema):
    page = fields.Int(load_default=1,  description='页码')
    size = fields.Int(load_default=10, description='每页个数')
    start_time = fields.Str(load_default=None, description='开始时间')
    end_time = fields.Str(load_default=None, description='结束时间')


class LiUploadSchemaRequests(ArgSchema):
    constant = fields.String(description='内容')


class LiSchemaResponse(BaseSchema):
    total = fields.Int(description='总数')
    items = fields.List(fields.Nested(LiSchema()))


class LiDlSchemaResponse(BaseSchema):
    msg = fields.Bool(description='是否删除成功')


class LiUploadSchemaResponse(BaseSchema):
    msg = fields.Bool(description='是否上传成功')
