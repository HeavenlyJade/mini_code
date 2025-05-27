from marshmallow import EXCLUDE
from marshmallow_dataclass import class_schema
from webargs import fields

from backend.mini_core.domain.t_user import ShopUser, ShopUserAddress
from kit.schema.base import (
    ArgSchema,
    BaseSchema,
    EntitySchema,
    ListQueryArgSchema,
    ListResultSchema,
)
from kit.schema.field import DateTimeDelimitedList

# ShopUser Schemas
ShopUserSchema = class_schema(ShopUser, base_schema=EntitySchema)


class ShopUserQueryArgSchema(ListQueryArgSchema):
    username = fields.Str(description='用户名')
    nickname = fields.Str(description='昵称')
    phone = fields.Str(description='手机号')
    email = fields.Str(description='邮箱')
    real_name = fields.Str(description='真实姓名')
    status = fields.Int(description='状态(1-正常,0-停用)')
    register_shop_id = fields.Int(description='所属门店ID')
    is_distributor = fields.Int(description='是否分销商(1-是,0-否)')
    gender = fields.Int(description='性别(0-未知,1-男,2-女)')
    member_level = fields.Str(description='会员等级')
    tags = fields.Str(description='标签')
    register_time = DateTimeDelimitedList(description='注册时间范围')
    points_min = fields.Int(description='积分下限')
    points_max = fields.Int(description='积分上限')
    balance_min = fields.Float(description='余额下限')
    balance_max = fields.Float(description='余额上限')
    # 排序规则：最新创建的数据在前
    ordering = fields.DelimitedList(fields.Str(), missing=['-create_time'])


class ShopUserListSchema(ListResultSchema):
    items = fields.List(fields.Nested(ShopUserSchema()))


class ShopUserCreateSchema(ShopUserSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'username',
            'nickname',
            'phone',
            'email',
            'password',
            'avatar',
            'openid',
            'unionid',
            'mini_program_name',
            'register_channel',
            'register_shop_id',
            'register_shop_name',
            'real_name',
            'gender',
            'birthday',
            'address',
            'member_level',
            'member_card_no',
            'points',
            'balance',
            'is_distributor',
            'tags',
            'remark',
            'status',
        )


class ShopUserUpdateSchema(ShopUserSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'nickname',
            'phone',
            'email',
            'avatar',
            'real_name',
            'gender',
            'birthday',
            'address',
            'member_level',
            'member_card_no',
            'points',
            'balance',
            'is_distributor',
            'tags',
            'remark',
            'status',
            "username",
        )

class WXShopUserUpdateSchema(ShopUserSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'nickname',
            'phone',
            'email',
            'avatar',
            'real_name',
            'gender',
            'birthday',
            'address',
            'member_card_no',
            'is_distributor',
            'tags',
            'remark',
            "username",
        )


class ShopUserPatchSchema(ShopUserSchema):
    class Meta:
        unknown = EXCLUDE
        fields = ('password', 'status')


class ShopWechatLoginSchema(ArgSchema):
    code = fields.Str(required=True, description='微信授权码')
    user_info = fields.Dict(description='用户信息')


class ShopLoginSchema(ArgSchema):
    username = fields.Str(required=True, description='用户名/手机号')
    password = fields.Str(required=True, description='密码')


class ShopTokenSchema(BaseSchema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    user_info = fields.Nested(ShopUserSchema())
    msg = fields.Str()
    code = fields.Int()


class RefreshTokenSchema(BaseSchema):
    access_token = fields.Str()
    code = fields.Int()


class ShopUserStatusSchema(ArgSchema):
    status = fields.Int(required=True, description='状态值(1-正常,0-停用)')


# ShopUserAddress Schemas
ShopUserAddressSchema = class_schema(ShopUserAddress, base_schema=EntitySchema)


class ShopUserAddressQueryArgSchema(ListQueryArgSchema):
    user_id = fields.Str(description='用户编号')
    receiver_name = fields.Str(description='收货人姓名')
    receiver_phone = fields.Str(description='收货人电话')
    is_default = fields.Int(description='是否默认地址(1-是,0-否)')
    # 排序规则：默认地址在前
    ordering = fields.DelimitedList(fields.Str(), missing=['-is_default', '-create_time'])


class ShopUserAddressListSchema(ListResultSchema):
    items = fields.List(fields.Nested(ShopUserAddressSchema()))


class ShopUserAddressCreateSchema(ShopUserAddressSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'user_id',
            'receiver_name',
            'receiver_phone',
            'province',
            'city',
            'district',
            'detail_address',
            'postal_code',
            'is_default',
        )


class ShopUserAddressUpdateSchema(ShopUserAddressSchema):
    class Meta:
        unknown = EXCLUDE
        fields = (
            'receiver_name',
            'receiver_phone',
            'province',
            'city',
            'district',
            'detail_address',
            'postal_code',
            'is_default',
        )


class ShopUserSchemaRe(ArgSchema):
    data = fields.Nested(ShopUserSchema())
    code = fields.Int()


class ShopUserAddressSchemaRe(ArgSchema):
    data = fields.Nested(ShopUserAddressSchema())
    code = fields.Int()


class SetDefaultAddressSchema(ArgSchema):
    address_id = fields.Int(required=True, description='地址ID')
