from marshmallow import validate, Schema, validates, ValidationError
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields


from backend.mini_core.domain.distributionWithdrawal import DistributionWithdrawal
from kit.schema.base import (
    EntitySchema,
    EntityIntSchema,
    ListQueryArgSchema,
    ListResultSchema,
)
from kit.schema.field import DateTimeDelimitedList

# 基本 Schema 类 - 使用 class_schema 自动生成
DistributionWithdrawalSchema = class_schema(DistributionWithdrawal, base_schema=EntitySchema)


# 提现申请查询参数 Schema
class DistributionWithdrawalQueryArgSchema(ListQueryArgSchema):
    user_id = webargs_fields.Str(description='用户ID')
    withdrawal_no = webargs_fields.Str(description='提现申请单号')
    status = webargs_fields.Int(description='状态(0:待审核,1:审核通过,2:审核拒绝,3:处理中,4:已完成,5:失败)',
                                validate=validate.OneOf([0, 1, 2, 3, 4, 5]))
    withdrawal_type = webargs_fields.Str(description='提现方式(微信/支付宝/银行卡)')
    handler_id = webargs_fields.Int(description='处理人ID')
    handler_name = webargs_fields.Str(description='处理人姓名')
    transaction_id = webargs_fields.Str(description='第三方交易流水号')
    apply_time = DateTimeDelimitedList(description='申请时间范围')
    audit_time = DateTimeDelimitedList(description='审核时间范围')
    complete_time = DateTimeDelimitedList(description='完成时间范围')
    min_apply_amount = webargs_fields.Float(description='最小申请金额')
    max_apply_amount = webargs_fields.Float(description='最大申请金额')
    min_actual_amount = webargs_fields.Float(description='最小实际金额')
    max_actual_amount = webargs_fields.Float(description='最大实际金额')
    # 默认排序：最新申请在前
    ordering = webargs_fields.DelimitedList(webargs_fields.Str(), missing=['-apply_time'])


# 提现申请创建参数 Schema
class DistributionWithdrawalCreateSchema(Schema):
    apply_amount = webargs_fields.Float(required=True, description='申请提现金额',
                                        validate=validate.Range(min=0.01))
    withdrawal_type = webargs_fields.Str(required=True, description='提现方式',
                                         validate=validate.OneOf(['微信', '支付宝', '银行卡']))
    account_info = webargs_fields.Dict(required=True, description='收款账户信息')
    remark = webargs_fields.Str(description='备注', validate=validate.Length(max=255))

    @validates('account_info')
    def validate_account_info(self, value):
        """验证收款账户信息"""
        if not isinstance(value, dict):
            raise ValidationError('收款账户信息必须是字典格式')

        # 根据提现方式验证必要字段
        required_fields = []
        if 'account' not in value:
            required_fields.append('account')
        if 'name' not in value:
            required_fields.append('name')

        if required_fields:
            raise ValidationError(f'收款账户信息缺少必要字段: {", ".join(required_fields)}')


# 提现申请更新参数 Schema
class DistributionWithdrawalUpdateSchema(Schema):
    status = webargs_fields.Int(description='状态',
                                validate=validate.OneOf([0, 1, 2, 3, 4, 5]))
    reject_reason = webargs_fields.Str(description='拒绝原因', validate=validate.Length(max=255))
    remark = webargs_fields.Str(description='备注', validate=validate.Length(max=255))
    transaction_id = webargs_fields.Str(description='第三方交易流水号', validate=validate.Length(max=100))
    actual_amount = webargs_fields.Float(description='实际到账金额',
                                         validate=validate.Range(min=0))
    fee_amount = webargs_fields.Float(description='手续费',
                                      validate=validate.Range(min=0))
    handler_name = webargs_fields.Str(description='处理人姓名', validate=validate.Length(max=50))

    @validates('reject_reason')
    def validate_reject_reason(self, value):
        """当状态为拒绝时，拒绝原因不能为空"""
        # 这个验证需要在业务层处理，因为需要同时检查status字段
        pass


# 提现申请审核参数 Schema
class DistributionWithdrawalAuditSchema(Schema):
    status = webargs_fields.Int(required=True, description='审核状态',
                                validate=validate.OneOf([1, 2]))  # 1:通过, 2:拒绝
    reject_reason = webargs_fields.Str(description='拒绝原因', validate=validate.Length(max=255))

    @validates('reject_reason')
    def validate_reject_reason(self, value):
        """审核拒绝时必须提供拒绝原因"""
        # 注意：这里无法直接访问status字段，需要在业务层验证
        pass


# 提现申请完成参数 Schema
class DistributionWithdrawalCompleteSchema(Schema):
    transaction_id = webargs_fields.Str(required=True, description='第三方交易流水号',
                                        validate=validate.Length(min=1, max=100))
    actual_amount = webargs_fields.Float(description='实际到账金额',
                                         validate=validate.Range(min=0))
    fee_amount = webargs_fields.Float(description='手续费',
                                      validate=validate.Range(min=0))


# 提现申请统计 Schema
class DistributionWithdrawalStatsSchema(Schema):
    total_count = webargs_fields.Int(description='总申请数')
    pending_count = webargs_fields.Int(description='待审核数')
    approved_count = webargs_fields.Int(description='已通过数')
    rejected_count = webargs_fields.Int(description='已拒绝数')
    completed_count = webargs_fields.Int(description='已完成数')
    total_apply_amount = webargs_fields.Float(description='总申请金额')
    total_actual_amount = webargs_fields.Float(description='总实际金额')
    total_fee_amount = webargs_fields.Float(description='总手续费')


# 用户提现汇总 Schema
class UserWithdrawalSummarySchema(Schema):
    user_id = webargs_fields.Str(description='用户ID')
    total_count = webargs_fields.Int(description='总提现次数')
    total_apply_amount = webargs_fields.Float(description='总申请金额')
    total_actual_amount = webargs_fields.Float(description='总实际到账金额')
    total_fee_amount = webargs_fields.Float(description='总手续费')
    pending_count = webargs_fields.Int(description='进行中的提现数')
    completed_amount = webargs_fields.Float(description='已完成提现金额')


# 响应 Schema
class DistributionWithdrawalResponseSchema(EntityIntSchema):
    data = webargs_fields.Nested(DistributionWithdrawalSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class DistributionWithdrawalListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(DistributionWithdrawalSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')
    message = webargs_fields.Str(description='消息')


class DistributionWithdrawalStatsResponseSchema(Schema):
    data = webargs_fields.Nested(DistributionWithdrawalStatsSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class UserWithdrawalSummaryResponseSchema(Schema):
    data = webargs_fields.Nested(UserWithdrawalSummarySchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


# 批量操作 Schema
class BatchWithdrawalUpdateSchema(Schema):
    withdrawal_ids = webargs_fields.List(webargs_fields.Int(), required=True, description='提现申请ID列表')
    status = webargs_fields.Int(required=True, description='目标状态',
                                validate=validate.OneOf([1, 2, 3, 4, 5]))
    reject_reason = webargs_fields.Str(description='拒绝原因（批量拒绝时使用）')


# 提现申请详情 Schema（包含关联信息）
class DistributionWithdrawalDetailSchema(DistributionWithdrawalSchema):
    """扩展的提现申请详情，包含用户信息等"""
    user_name = webargs_fields.Str(description='用户姓名')
    user_mobile = webargs_fields.Str(description='用户手机号')
    distribution_level = webargs_fields.Str(description='分销等级')


class DistributionWithdrawalDetailResponseSchema(Schema):
    data = webargs_fields.Nested(DistributionWithdrawalDetailSchema())
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')
