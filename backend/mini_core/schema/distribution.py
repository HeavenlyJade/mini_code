from marshmallow import validate
from marshmallow_dataclass import class_schema
from webargs import fields

from backend.mini_core.domain.distribution import (Distribution, DistributionConfig,
                                                   DistributionGrade, DistributionGradeUpdate,
                                                   DistributionIncome, DistributionLog)
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema,ArgSchema

# 基本 Schema 类
DistributionSchema = class_schema(Distribution, base_schema=EntitySchema)
DistributionConfigSchema = class_schema(DistributionConfig, base_schema=EntitySchema)
DistributionGradeSchema = class_schema(DistributionGrade, base_schema=EntitySchema)
DistributionGradeUpdateSchema = class_schema(DistributionGradeUpdate, base_schema=EntitySchema)
DistributionIncomeSchema = class_schema(DistributionIncome, base_schema=EntitySchema)
DistributionLogSchema = class_schema(DistributionLog, base_schema=EntitySchema)


# 分销查询参数 Schema
class DistributionQueryArgSchema(EntityIntSchema):
    sn = fields.Str(description='编号')
    real_name = fields.Str(description='真实姓名')
    ser_name = fields.Str(description='字用户对搜索名称')
    mobile = fields.Str(description='手机号')
    # user_id = fields.Str(description='用户ID')
    grade_id = fields.Int(description='等级ID')
    status = fields.Int(description='状态',)


# 分销配置查询参数 Schema
class DistributionConfigQueryArgSchema(EntityIntSchema):
    key = fields.Str(description='配置项')


# 分销等级查询参数 Schema
class DistributionGradeQueryArgSchema(EntityIntSchema):
    name = fields.Str(description='等级名称')


# 分销等级更新查询参数 Schema
class DistributionGradeUpdateQueryArgSchema(EntityIntSchema):
    grade_id = fields.Int(description='等级ID')
    key = fields.Str(description='条件名称')


# 分销收入查询参数 Schema
class DistributionIncomeQueryArgSchema(EntityIntSchema):
    user_id = fields.Str(description='用户ID')
    order_id = fields.Str(description='订单ID')
    product_id = fields.Str(description='产品ID')
    product_name = fields.Str(description='产品名称')
    grade_id = fields.Int(description='分销等级ID')
    start_date = fields.Str(description='开始时间')
    end_date = fields.Str(description='结束时间')
    status = fields.Int(description='状态', validate=validate.OneOf([-1, 0, 1, 2, 3]))


# 分销日志查询参数 Schema
class DistributionLogQueryArgSchema(EntityIntSchema):
    distribution_id = fields.Int(description='分销ID')
    change_object = fields.Str(description='变更对象')
    change_type = fields.Str(description='变更类型')
    source_id = fields.Int(description='来源ID')
    admin_id = fields.Int(description='管理员ID')
    user_id = fields.Str(description='变更类型')
    start_date = fields.Str(description='开始时间')
    end_date = fields.Str(description='结束时间')


# 分销用户视图 Schema
class DistributionUserSchema(EntityIntSchema):
    sn = fields.Str(description='编号')
    real_name = fields.Str(description='真实姓名')
    mobile = fields.Str(description='手机号')
    identity = fields.Int(description='身份')
    user_id = fields.Str(description='用户ID')
    user_father_id = fields.Int(description='上级ID')
    grade_id = fields.Int(description='等级ID')
    grade_name = fields.Str(description='等级名称')
    status = fields.Int(description='状态')


# 分销等级详情 Schema
class DistributionGradeDetailSchema(EntityIntSchema):
    name = fields.Str(description='等级名称')
    weight = fields.Int(description='权重')
    self_ratio = fields.Decimal(description='自购比例')
    first_ratio = fields.Decimal(description='一级分拥比例')
    second_ratio = fields.Decimal(description='二级分拥比例')
    conditions = fields.Decimal(description="条件")
    update_relation = fields.Int(description='分销关系')
    remark =fields.Str(description='等级描述')


class DistributionGradSchema(EntityIntSchema):
    name = fields.Str(description='等级名称')
    weight = fields.Int(description='权重')
    self_ratio = fields.Decimal(description='自购比例')
    first_ratio = fields.Decimal(description='一级分拥比例')
    second_ratio = fields.Decimal(description='二级分拥比例')
    update_relation = fields.Int(description='分销关系')


# 分销收入汇总 Schema
class DistributionIncomeSummarySchema(EntityIntSchema):
    user_id = fields.Str(description='用户ID')
    total_money = fields.Decimal(description='总收入')
    pending_money = fields.Decimal(description='待结算金额')
    settled_money = fields.Decimal(description='已结算金额')
    frozen_money = fields.Decimal(description='已冻结金额')


# 响应 Schema
class ReDistributionSchemaList(ArgSchema):
    data = fields.List(fields.Nested(DistributionUserSchema()))
    code = fields.Int(description='状态')
    total = fields.Int(description='总数')

class ReDistributionSchema(EntityIntSchema):
    data = fields.Nested(DistributionUserSchema())
    code = fields.Int(description='状态')


class ReDistributionConfigSchema(EntityIntSchema):
    data = fields.List(fields.Nested(DistributionConfigSchema()))
    # data = fields.Nested(DistributionConfigSchema())
    code = fields.Int(description='状态')

class ReDistributionConfigDataSchema(EntityIntSchema):
    data = fields.Nested(DistributionConfigSchema())
    code = fields.Int(description='状态')


class ReDistributionGradeSchema(EntityIntSchema):
    data = fields.Nested(DistributionGradeDetailSchema())
    code = fields.Int(description='状态')


class ReDistributionGradeListSchema(EntityIntSchema):
    data = fields.List(fields.Nested(DistributionGradeDetailSchema()))
    code = fields.Int(description='状态')

class ReDistributionIncomeSchema(ListResultSchema):
    data = fields.List(fields.Nested(DistributionIncomeSchema()))
    code = fields.Int(description='状态')


class ReDistributionWxDataSchema(EntitySchema):
    config_data =fields.List(fields.Nested(DistributionConfigSchema()))
    grade_data = fields.List(fields.Nested(DistributionGradeSchema()))
    distribution_user_data = fields.Nested(DistributionSchema())
