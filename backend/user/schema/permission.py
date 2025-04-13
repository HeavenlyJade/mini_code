from marshmallow import EXCLUDE
from marshmallow_dataclass import class_schema
from webargs import fields

from backend.user.domain.permission import Permission
from kit.schema.base import (
    ArgSchema,
    EntitySchema,
    ListQueryArgSchema,
    ListResultSchema,
)
from kit.schema.field import RequiredStr

PermissionSchema = class_schema(Permission, base_schema=EntitySchema)


class PermissionQueryArgSchema(ListQueryArgSchema):
    name = fields.Str(description='权限名称')
    number = fields.Str(description='权限编号')
    parent_id = fields.Int(description='父权限ID')
    level = fields.Int(description='权限等级')
    menu_type = fields.Int(description='菜单类型(0:菜单,1:按钮)')
    status = fields.Int(description='状态(0:禁用,1:启用)')
    # 排序规则：按level和sort_order排序
    ordering = fields.DelimitedList(fields.Str(), missing=['level', 'sort_order'])


class PermissionListSchema(ListResultSchema):
    items = fields.List(fields.Nested(PermissionSchema()))


class PermissionCreateSchema(PermissionSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'name',
            'number',
            'parent_id',
            'level',
            'path',
            'component',
            'icon',
            'menu_type',
            'perms',
            'status',
            'sort_order',
            'description',
        )


class PermissionUpdateSchema(PermissionSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'name',
            'parent_id',
            'level',
            'path',
            'component',
            'icon',
            'menu_type',
            'perms',
            'status',
            'sort_order',
            'description',
        )


class PermissionTreeNodeSchema(ArgSchema):
    id = fields.Int(description='权限ID')
    name = fields.Str(description='权限名称')
    number = fields.Str(description='权限编号')
    level = fields.Int(description='权限等级')
    path = fields.Str(description='权限路径')
    component = fields.Str(description='对应前端组件')
    icon = fields.Str(description='图标')
    menu_type = fields.Int(description='菜单类型(0:菜单,1:按钮)')
    perms = fields.Str(description='权限标识')
    status = fields.Int(description='状态(0:禁用,1:启用)')
    sort_order = fields.Int(description='排序号')
    children = fields.List(fields.Nested(lambda: PermissionTreeNodeSchema()), description='子权限')


class PermissionTreeSchema(ListResultSchema):
    items = fields.List(fields.Nested(PermissionTreeNodeSchema()))
