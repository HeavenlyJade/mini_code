from flask.views import MethodView

from backend.mini_core.schema.order.order_log import (
    OrderLogQueryArgSchema, OrderLogResponseSchema, OrderLogListResponseSchema,
    OrderLogCreateSchema, OrderLogBatchQueryArgSchema, OrderLogStatisticsQueryArgSchema,
    OperatorLogQueryArgSchema, LogSearchQueryArgSchema, OrderLogStatisticsResponseSchema
)
from backend.mini_core.service import order_log_service
from backend.business.service.auth import auth_required
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('order_log', 'order_log', url_prefix='/')


@blp.route('/order-logs')
class OrderLogAPI(MethodView):
    """订单日志API"""
    decorators = [auth_required()]

    @blp.arguments(OrderLogQueryArgSchema, location='query')
    @blp.response(OrderLogListResponseSchema)
    def get(self, args: dict):
        """查询订单日志列表"""
        return order_log_service.list(args)

    @blp.arguments(OrderLogCreateSchema)
    @blp.response(OrderLogResponseSchema)
    def post(self, log):
        """创建订单日志"""
        return order_log_service.create_log(log)


@blp.route('/order-logs/batch')
class OrderLogBatchAPI(MethodView):
    """批量订单日志API"""
    decorators = [auth_required()]

    @blp.arguments(OrderLogBatchQueryArgSchema)
    @blp.response(OrderLogListResponseSchema)
    def get(self, args):
        """批量查询多个订单的日志"""
        # 将order_nos添加到in_query_params查询
        query_args = {
            'order_no': args.pop('order_nos'),
            'need_total_count': True
        }

        # 添加其他查询参数
        if 'operation_type' in args:
            query_args['operation_type'] = args['operation_type']

        # 添加时间范围查询
        if 'start_time' in args or 'end_time' in args:
            time_range = []
            if 'start_time' in args:
                time_range.append(args['start_time'])
            if 'end_time' in args:
                time_range.append(args['end_time'])
            query_args['operation_time'] = time_range

        return order_log_service.list(query_args)

    @blp.arguments(OrderLogCreateSchema(many=True))
    def post(self, logs):
        """批量创建订单日志"""
        return order_log_service.batch_create_logs(logs)


@blp.route('/order-logs/<int:log_id>')
class OrderLogByIDAPI(MethodView):
    """订单日志详情API"""
    decorators = [auth_required()]

    @blp.response(OrderLogResponseSchema)
    def get(self, log_id: int):
        """获取指定ID的订单日志"""
        return dict(data=order_log_service.get(log_id), code=200)


@blp.route('/orders/<string:order_no>/logs')
class OrderLogsByOrderAPI(MethodView):
    """订单的日志API"""
    decorators = [auth_required()]

    @blp.response(OrderLogListResponseSchema)
    def get(self, order_no: str):
        """获取指定订单的所有日志"""
        return order_log_service.get_order_logs(order_no)


@blp.route('/orders/<string:order_no>/logs/<string:operation_type>')
class OrderLogsByTypeAPI(MethodView):
    """订单特定类型的日志API"""
    decorators = [auth_required()]

    @blp.response(OrderLogListResponseSchema)
    def get(self, order_no: str, operation_type: str):
        """获取指定订单的特定类型日志"""
        return order_log_service.get_order_logs_by_type(order_no, operation_type)


@blp.route('/order-logs/latest')
class LatestOrderLogsAPI(MethodView):
    """最新订单日志API"""
    decorators = [auth_required()]

    @blp.response(OrderLogListResponseSchema)
    def get(self):
        """获取最新的订单日志"""
        return order_log_service.get_latest_logs()


@blp.route('/order-logs/operators')
class OperatorLogsAPI(MethodView):
    """操作人日志API"""
    decorators = [auth_required()]

    @blp.arguments(OperatorLogQueryArgSchema, location='query')
    @blp.response(OrderLogListResponseSchema)
    def get(self, args):
        """获取指定操作人的操作日志"""
        return order_log_service.get_operator_logs(args)


@blp.route('/order-logs/search')
class LogSearchAPI(MethodView):
    """日志搜索API"""
    decorators = [auth_required()]

    @blp.arguments(LogSearchQueryArgSchema, location='query')
    @blp.response(OrderLogListResponseSchema)
    def get(self, args):
        """搜索操作日志"""
        return order_log_service.search_logs(args['search_term'])


@blp.route('/order-logs/statistics')
class LogStatisticsAPI(MethodView):
    """日志统计API"""
    decorators = [auth_required()]

    @blp.arguments(OrderLogStatisticsQueryArgSchema, location='query')
    @blp.response(OrderLogStatisticsResponseSchema)
    def get(self, args):
        """获取操作日志统计数据"""
        return order_log_service.get_statistics(args)
