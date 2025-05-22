from marshmallow import Schema, fields
from webargs import fields as webargs_fields

from kit.schema.base import EntitySchema, ListResultSchema, ListQueryArgSchema

# 基本 Schema 类 - 完全避免 Decimal 类型
class MemberLevelConfigSchema(EntitySchema):
    level_code = fields.Str(description='等级代码')
    level_name = fields.Str(description='等级名称')
    level_value = fields.Int(description='等级数值')
    upgrade_condition_type = fields.Int(description='升级条件类型')
    upgrade_amount = fields.Float(description='升级所需消费金额', allow_none=True)
    upgrade_count = fields.Int(description='升级所需消费次数')
    upgrade_invite_count = fields.Int(description='升级所需邀请人数')
    discount_rate = fields.Float(description='会员折扣率', allow_none=True)
    point_ratio = fields.Float(description='积分倍率', allow_none=True)
    level_icon = fields.Str(description='等级图标URL', allow_none=True)
    level_color = fields.Str(description='等级颜色', allow_none=True)
    level_description = fields.Str(description='等级描述', allow_none=True)
    benefits = fields.Str(description='会员权益', allow_none=True)
    is_enabled = fields.Bool(description='是否启用')
    sort_order = fields.Int(description='排序')
    creator = fields.Str(description='创建人', allow_none=True)
    updater = fields.Str(description='更新人', allow_none=True)


# 会员等级配置查询参数 Schema
class MemberLevelConfigQueryArgSchema(ListQueryArgSchema):
    level_code = webargs_fields.Str(description='等级代码')
    level_name = webargs_fields.Str(description='等级名称')
    level_value = webargs_fields.Int(description='等级数值')
    upgrade_condition_type = webargs_fields.Int(description='升级条件类型')
    is_enabled = webargs_fields.Bool(description='是否启用')
    ordering = webargs_fields.DelimitedList(webargs_fields.Str(), missing=['level_value'])


# 会员等级配置创建参数 Schema
class MemberLevelConfigCreateSchema(Schema):
    level_code = webargs_fields.Str(required=True, description='等级代码')
    level_name = webargs_fields.Str(required=True, description='等级名称')
    level_value = webargs_fields.Int(required=True, description='等级数值')
    upgrade_condition_type = webargs_fields.Int(description='升级条件类型', missing=1)
    upgrade_amount = webargs_fields.Float(description='升级所需消费金额', missing=0)
    upgrade_count = webargs_fields.Int(description='升级所需消费次数', missing=0)
    upgrade_invite_count = webargs_fields.Int(description='升级所需邀请人数', missing=0)
    discount_rate = webargs_fields.Float(description='会员折扣率', missing=100)
    point_ratio = webargs_fields.Float(description='积分倍率', missing=1)
    level_icon = webargs_fields.Str(description='等级图标URL')
    level_color = webargs_fields.Str(description='等级颜色')
    level_description = webargs_fields.Str(description='等级描述')
    benefits = webargs_fields.Raw(description='会员权益(JSON格式)')
    is_enabled = webargs_fields.Bool(description='是否启用', missing=True)
    sort_order = webargs_fields.Int(description='排序', missing=0)


# 会员等级配置更新参数 Schema
class MemberLevelConfigUpdateSchema(Schema):
    level_code = webargs_fields.Str(description='等级代码')
    level_name = webargs_fields.Str(description='等级名称')
    level_value = webargs_fields.Int(description='等级数值')
    upgrade_condition_type = webargs_fields.Int(description='升级条件类型')
    upgrade_amount = webargs_fields.Float(description='升级所需消费金额')
    upgrade_count = webargs_fields.Int(description='升级所需消费次数')
    upgrade_invite_count = webargs_fields.Int(description='升级所需邀请人数')
    discount_rate = webargs_fields.Float(description='会员折扣率')
    point_ratio = webargs_fields.Float(description='积分倍率')
    level_icon = webargs_fields.Str(description='等级图标URL')
    level_color = webargs_fields.Str(description='等级颜色')
    level_description = webargs_fields.Str(description='等级描述')
    benefits = webargs_fields.Raw(description='会员权益(JSON格式)')
    is_enabled = webargs_fields.Bool(description='是否启用')
    sort_order = webargs_fields.Int(description='排序')


# 响应 Schema
class MemberLevelConfigResponseSchema(Schema):
    data = webargs_fields.Nested(MemberLevelConfigSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class MemberLevelConfigListResponseSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(MemberLevelConfigSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')
