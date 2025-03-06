from marshmallow import EXCLUDE, post_load, post_dump, pre_dump
from marshmallow_dataclass import class_schema
from webargs import fields

from backend.user.domain.user import User
from kit.schema.base import (
    ArgSchema,
    BaseSchema,
    EntitySchema,
    ListQueryArgSchema,
    ListResultSchema,
)

_UserSchema = class_schema(User, base_schema=EntitySchema)


class UserSchema(_UserSchema):
    role_numbers = fields.Raw()

    @post_load
    def post_load(self, data, **kwargs):
        if 'role_numbers' in data:
            role_numbers = data['role_numbers']
            if role_numbers:
                data['role_numbers'] = role_numbers[0]
            else:
                data['role_numbers'] = None
        return data

    @post_dump
    def post_dump(self, data: dict, **kwargs):
        if data['role_numbers']:
            data['role_numbers'] = [data['role_numbers']]
        else:
            data['role_numbers'] = []
        return data


class UserQueryArgSchema(ListQueryArgSchema):
    username = fields.Str(description='用户名')
    department = fields.Str(description='部门')
    job_title = fields.Str(description='职务')
    department_id = fields.Int(description='部门ID')
    role_number = fields.Str()
    # 排序规则：最新创建的数据在前
    ordering = fields.DelimitedList(fields.Str(), missing=['-create_time'])


class UserListSchema(ListResultSchema):
    items = fields.List(fields.Nested(UserSchema()))


class UserCreateSchema(UserSchema):
    ...


class UserUpdateSchema(UserSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'department_id',
            'job_title',
            'mobile',
            'email',
            'role_numbers',
        )


class UserPatchSchema(UserSchema):
    class Meta:
        unknown = EXCLUDE
        fields = ('password',)


class LoginSchema(ArgSchema):
    username = fields.Str(required=True, description='用户名')
    password = fields.Str(required=True, description='密码')


class TokenSchema(BaseSchema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    msg = fields.Str()
    code = fields.Int()


class RefreshTokenSchema(BaseSchema):
    access_token = fields.Str()


class UserCenterUpdateSchema(UserSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'mobile',
            'email',
            'password',
        )
