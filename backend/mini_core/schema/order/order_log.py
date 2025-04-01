from marshmallow import Schema
from marshmallow_dataclass import class_schema
from webargs import fields as webargs_fields

from backend.mini_core.domain.order.order_log import OrderLog
from kit.schema.base import EntitySchema, EntityIntSchema, ListResultSchema, ListQueryArgSchema
from kit.schema.field import DateTimeDelimitedList

# 基本 Schema 类 - 使用 class_schema 自动生成
OrderLogSchema = class_schema(OrderLog, base_schema=EntitySchema)


# 订单日志查询参数 Schema
class OrderLogQueryArgSchema(ListQueryArgSchema):
    order_no = webargs_fields.Str(description='订单编号')
    operation_type = webargs_fields.Str(description='操作类型')
    operation_desc = webargs_fields.Str(description='操作描述')
    operator = webargs_fields.Str(description='操作人')
    operation_time = DateTimeDelimitedList(description='操作时间范围')
    remark = webargs_fields.Str(description='备注')
    # 默认按操作时间倒序排序
    ordering = webargs_fields.DelimitedList(webargs_fields.Str(), missing=['-operation_time'])


# 订单日志创建参数 Schema
class OrderLogCreateSchema(Schema):
    order_no = webargs_fields.Str(required=True, description='订单编号')
    operation_type = webargs_fields.Str(required=True, description='操作类型')
    operation_desc = webargs_fields.Str(required=True, description='操作描述')
    operator = webargs_fields.Str(required=True, description='操作人')
    operation_time = webargs_fields.DateTime(description='操作时间')
    operation_ip = webargs_fields.Str(description='操作IP')
    old_value = webargs_fields.Str(description='修改前值')
    new_value = webargs_fields.Str(description='修改后值')
    remark = webargs_fields.Str(description='备注')


# 订单日志批量查询参数 Schema
class OrderLogBatchQueryArgSchema(Schema):
    order_nos = webargs_fields.List(webargs_fields.Str(), required=True, description='订单编号列表')
    operation_type = webargs_fields.Str(description='操作类型')
    start_time = webargs_fields.DateTime(description='开始时间')
    end_time = webargs_fields.DateTime(description='结束时间')


# 订单日志统计参数 Schema
class OrderLogStatisticsQueryArgSchema(Schema):
    start_time = webargs_fields.DateTime(description='开始时间')
    end_time = webargs_fields.DateTime(description='结束时间')
    operation_type = webargs_fields.Str(description='操作类型')


# 操作人日志查询参数 Schema
class OperatorLogQueryArgSchema(Schema):
    operator = webargs_fields.Str(required=True, description='操作人')
    start_time = webargs_fields.DateTime(description='开始时间')
    end_time = webargs_fields.DateTime(description='结束时间')


# 日志搜索参数 Schema
class LogSearchQueryArgSchema(Schema):
    search_term = webargs_fields.Str(required=True, description='搜索关键词')


# 响应 Schema
class OrderLogResponseSchema(EntityIntSchema):
    data = webargs_fields.Nested(OrderLogSchema())
    code = webargs_fields.Int(description='状态码')


class OrderLogListResponseSchema(ListResultSchema):
    data = webargs_fields.List(webargs_fields.Nested(OrderLogSchema()))
    code = webargs_fields.Int(description='状态码')
    total = webargs_fields.Int(description='总数')


# 统计结果响应 Schema
class OrderLogStatisticsSchema(Schema):
    total_logs = webargs_fields.Int(description='日志总数')
    logs_by_type = webargs_fields.Dict(keys=webargs_fields.Str(),
                                     values=webargs_fields.Int(),
                                     description='各类型日志数量')


class OrderLogStatisticsResponseSchema(Schema):
    data = webargs_fields.Nested(OrderLogStatisticsSchema())
    code = webargs_fields.Int(description='状态码')
