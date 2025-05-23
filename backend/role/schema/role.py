from marshmallow import EXCLUDE
from marshmallow_dataclass import class_schema
from webargs import fields

from backend.role.domain.role import Role
from kit.schema.base import (
    ArgSchema,
    EntitySchema,
    ListQueryArgSchema,
    ListResultSchema,
)
from kit.schema.field import RequiredStr

RoleSchema = class_schema(Role, base_schema=EntitySchema)


class RoleQueryArgSchema(ListQueryArgSchema):
    role_number = fields.Str(description='角色编码')
    creator = fields.Str(description='创建者')
    modifier = fields.Str(description='修改者')
    # 排序规则：最新创建的数据在前
    ordering = fields.DelimitedList(fields.Str(), missing=['-create_time'])


class RoleListSchema(ListResultSchema):
    items = fields.List(fields.Nested(RoleSchema()))


class RoleCreateSchema(RoleSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'role_number',
        )




class RoleUpdateSchema(ArgSchema):
    role_number = fields.Str(description='角色编码')
    permission_ids = fields.List(fields.Int,description='权限ids')
    # class Meta:
    #     unknown = EXCLUDE
    #     fields = (
    #         'role_number',
    #         'access_level',
    #         'operation_terminal',
    #         'allowed_department_ids',
    #         'areas',
    #         'permission_ids',  # 添加这一行
    #         'creator',
    #         'modifier',
    #     )
