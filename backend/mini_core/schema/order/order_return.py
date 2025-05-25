from marshmallow import validate, Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.order_return import OrderReturn, OrderReturnDetail, OrderReturnLog
from kit.schema.base import EntitySchema, ListResultSchema, ListQueryArgSchema

# 基本 Schema 类 - 使用 class_schema 自动生成
OrderReturnSchema = class_schema(OrderReturn, base_schema=EntitySchema)
OrderReturnDetailSchema = class_schema(OrderReturnDetail, base_schema=EntitySchema)
OrderReturnLogSchema = class_schema(OrderReturnLog, base_schema=EntitySchema)


# 订单退货查询参数 Schema
class OrderReturnQueryArgSchema(ListQueryArgSchema):
    return_no = webargs_fields.Str(description='退货单号')
    order_no = webargs_fields.Str(description='关联订单编号')
    user_id = webargs_fields.Int(description='用户ID')
    return_type = webargs_fields.Str(description='退货类型(退货退款/仅退款)')
    status = webargs_fields.Str(description='退货状态')
    return_reason_id = webargs_fields.Int(description='退货原因ID')
    return_reason = webargs_fields.Str(description='退货原因描述')
    return_express_no = webargs_fields.Str(description='退货快递单号')
    process_username = webargs_fields.Str(description='处理人用户名')
    start_time = webargs_fields.DateTime(description='申请开始时间')
    end_time = webargs_fields.DateTime(description='申请结束时间')
    audit_start_time = webargs_fields.DateTime(description='审核开始时间')
    audit_end_time = webargs_fields.DateTime(description='审核结束时间')
    complete_start_time = webargs_fields.DateTime(description='完成开始时间')
    complete_end_time = webargs_fields.DateTime(description='完成结束时间')
    min_amount = webargs_fields.Decimal(description='最小退款金额')
    max_amount = webargs_fields.Decimal(description='最大退款金额')
    keyword = webargs_fields.Str(description='关键词搜索')


# 退货明细查询参数 Schema
class OrderReturnDetailQueryArgSchema(ListQueryArgSchema):
    return_id = webargs_fields.Int(description='退货单ID')
    order_detail_id = webargs_fields.Int(description='订单详情ID')
    product_id = webargs_fields.Int(description='商品ID')
    sku_id = webargs_fields.Str(description='SKU ID')
    product_name = webargs_fields.Str(description='商品名称')


# 退货日志查询参数 Schema
class OrderReturnLogQueryArgSchema(ListQueryArgSchema):
    return_id = webargs_fields.Int(description='退货单ID')
    return_no = webargs_fields.Str(description='退货单号')
    operation_type = webargs_fields.Str(description='操作类型')
    operator = webargs_fields.Str(description='操作人')
    start_time = webargs_fields.DateTime(description='操作开始时间')
    end_time = webargs_fields.DateTime(description='操作结束时间')


# 创建退货单参数 Schema
class CreateReturnSchema(Schema):
    order_no = webargs_fields.Str(required=True, description='关联订单编号')
    id = webargs_fields.Int(required=True, description='订单ID')
    order_item_id = webargs_fields.Str(required=True, description='订单详情下的子分类id')


class ReturnApplicationSchema(Schema):
    order_no = webargs_fields.Str(allow_none=True, description='订单号')
    return_detail = webargs_fields.List(webargs_fields.Nested(CreateReturnSchema()), description='退货订单详情')
    reason = webargs_fields.Str(allow_none=True, description='退货理由')


class AuditReturnSchema(Schema):
    status = webargs_fields.Int(required=True, description='退货状态(0待审核/1已同意/2已拒绝/3退款中/4已完成)',
                                validate=validate.OneOf([0, 1, 2, 3, 4,5]))
    refuse_reason = webargs_fields.Str(allow_none=True, description='拒绝原因')
    admin_remark = webargs_fields.Str(allow_none=True, description='管理员备注')
    process_user_id = webargs_fields.Int(dump_only=True, description='处理人ID')
    process_username = webargs_fields.Str(dump_only=True, description='处理人用户名')


# 更新物流信息参数 Schema
class UpdateShippingInfoSchema(Schema):
    return_express_company = webargs_fields.Str(required=True, description='退货快递公司')
    return_express_no = webargs_fields.Str(required=True, description='退货快递单号')


class ReturnOrder(Schema):
    status = webargs_fields.Int(description='退货状态')


# 完成退款参数 Schema
class CompleteRefundSchema(Schema):
    refund_way = webargs_fields.Str(description='实际退款方式')
    admin_remark = webargs_fields.Str(description='管理员备注')


# 退货统计信息 Schema
class ReturnTypeStatsSchema(Schema):
    type = webargs_fields.Str(description='退货类型')
    count = webargs_fields.Int(description='数量')


class ReturnStatsSchema(Schema):
    total = webargs_fields.Int(description='总退货单数')
    pending_audit = webargs_fields.Int(description='待审核数')
    approved = webargs_fields.Int(description='已同意数')
    rejected = webargs_fields.Int(description='已拒绝数')
    in_refund = webargs_fields.Int(description='退款中数')
    completed = webargs_fields.Int(description='已完成数')
    today_returns = webargs_fields.Int(description='今日退货申请数')
    today_refund = webargs_fields.Float(description='今日退款金额')
    type_stats = webargs_fields.List(webargs_fields.Nested(ReturnTypeStatsSchema()), description='类型统计')


# 月度退货统计 Schema
class MonthlyReturnStatsSchema(Schema):
    month = webargs_fields.Str(description='月份')
    return_count = webargs_fields.Int(description='退货数')
    total_refund = webargs_fields.Float(description='退款总额')


# 完整退货单详情 Schema (包含明细和日志)
class CompleteReturnDetailSchema(Schema):
    return_info = webargs_fields.Nested(OrderReturnSchema)
    return_details = webargs_fields.List(webargs_fields.Nested(OrderReturnDetailSchema))
    return_logs = webargs_fields.List(webargs_fields.Nested(OrderReturnLogSchema))


# 响应 Schema
class ReOrderReturnSchema(Schema):
    data = webargs_fields.Nested(OrderReturnSchema)
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class ReOrderReturnListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(OrderReturnSchema))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


class ReCompleteReturnDetailSchema(Schema):
    data = webargs_fields.Nested(CompleteReturnDetailSchema)
    code = webargs_fields.Int(description='状态码')
    message = webargs_fields.Str(description='消息')


class ReOrderReturnDetailListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(OrderReturnDetailSchema))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


class ReOrderReturnLogListSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(OrderReturnLogSchema))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


class ReReturnStatsSchema(Schema):
    data = webargs_fields.Nested(ReturnStatsSchema)
    code = webargs_fields.Int(description='状态码')


class ReMonthlyReturnStatsSchema(Schema):
    data = webargs_fields.List(webargs_fields.Nested(MonthlyReturnStatsSchema))
    code = webargs_fields.Int(description='状态码')
