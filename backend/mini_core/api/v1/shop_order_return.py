from flask.views import MethodView

from backend.mini_core.schema.order.order_return import (
    OrderReturnQueryArgSchema, ReOrderReturnSchema, ReOrderReturnListSchema,
    OrderReturnDetailQueryArgSchema, ReOrderReturnDetailListSchema,
    OrderReturnLogQueryArgSchema, ReOrderReturnLogListSchema,
    ReturnApplicationSchema, AuditReturnSchema, UpdateShippingInfoSchema,
    CompleteRefundSchema, ReCompleteReturnDetailSchema,ReturnOrder,
    ReReturnStatsSchema, ReMonthlyReturnStatsSchema
)
from backend.business.service.auth import auth_required
from backend.mini_core.service import order_return_service, order_return_detail_service, order_return_log_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('order_return', 'order_return', url_prefix='/')


@blp.route('/shop-order-return')
class OrderReturnAPI(MethodView):
    """订单退货API"""
    decorators = [auth_required()]

    @blp.arguments(OrderReturnQueryArgSchema, location='query')
    @blp.response(ReOrderReturnListSchema)
    def get(self, args: dict):
        """查询退货单列表"""
        return order_return_service.get_return_list(args)

    @blp.arguments(ReturnApplicationSchema)
    @blp.response(ReOrderReturnSchema)
    def post(self, application):
        """创建退货申请"""
        return order_return_service.create_return(application["return_info"], application["return_items"])


@blp.route('/shop-order-return_detail')
class OrderReturnDetailAPI(MethodView):
    """退货单详情API"""
    decorators = [auth_required()]

    @blp.arguments(OrderReturnQueryArgSchema, location='query')
    @blp.response(ReCompleteReturnDetailSchema)
    def get(self, args: dict):
        """获取指定订单号的退货单详情"""
        return order_return_service.get_return_by_order_no(args["order_no"])


@blp.route('/shop-order-return/by-return-no/<string:return_no>')
class OrderReturnByReturnNoAPI(MethodView):
    """通过退货单号查询退货单API"""
    decorators = [auth_required()]

    @blp.response(ReCompleteReturnDetailSchema)
    def get(self, return_no: str):
        """通过退货单号获取退货单详情"""
        return order_return_service.get_return_by_no(return_no)

@blp.route('/shop-order-return/by-order-no/<string:order_no>')
class OrderReturnsByOrderNoAPI(MethodView):
    """通过订单号查询退货单API"""
    decorators = [auth_required()]

    @blp.response(ReOrderReturnListSchema)
    def get(self, order_no: str):
        """通过订单号获取相关的退货单"""
        return order_return_service.get_returns_by_order(order_no)


@blp.route('/shop-order-return/user/<int:user_id>')
class UserOrderReturnsAPI(MethodView):
    """用户退货单API"""
    decorators = [auth_required()]

    @blp.response(ReOrderReturnListSchema)
    def get(self, user_id: int):
        """获取用户的所有退货单"""
        return order_return_service.get_user_returns(user_id)


@blp.route('/shop-order-return/stats')
class OrderReturnStatsAPI(MethodView):
    """退货统计API"""
    decorators = [auth_required()]

    @blp.response(ReReturnStatsSchema)
    def get(self):
        """获取退货统计信息"""
        return order_return_service.get_return_stats()


@blp.route('/shop-order-return/monthly-stats')
class MonthlyReturnStatsAPI(MethodView):
    """月度退货统计API"""
    decorators = [auth_required()]

    @blp.response(ReMonthlyReturnStatsSchema)
    def get(self):
        """获取月度退货统计"""
        return order_return_service.get_monthly_stats()


@blp.route('/shop-order-return/<string:order_no>/audit')
class AuditOrderReturnAPI(MethodView):
    """审核退货单API"""
    decorators = [auth_required()]

    @blp.arguments(AuditReturnSchema)
    @blp.response(ReOrderReturnSchema)
    def put(self, args, order_no: str):
        """审核退货单"""
        status = args.pop("status")
        return order_return_service.update_return_status(order_no, status, **args)


@blp.route('/shop-order-return/<int:return_id>/shipping')
class UpdateReturnShippingAPI(MethodView):
    """更新退货物流信息API"""
    decorators = [auth_required()]

    @blp.arguments(UpdateShippingInfoSchema)
    @blp.response(ReOrderReturnSchema)
    def post(self, args, return_id: int):
        """更新退货物流信息"""
        return order_return_service.update_shipping_info(
            return_id,
            args["return_express_company"],
            args["return_express_no"]
        )


@blp.route('/shop-order-return/<int:return_id>/complete')
class CompleteReturnRefundAPI(MethodView):
    """完成退款API"""
    decorators = [auth_required()]

    @blp.arguments(CompleteRefundSchema)
    @blp.response(ReOrderReturnSchema)
    def post(self, args, return_id: int):
        """标记退款完成"""
        return order_return_service.update_return_status(return_id, "已完成", **args)


@blp.route('/shop-order-return-detail')
class OrderReturnDetailListAPI(MethodView):
    """退货商品明细API"""
    decorators = [auth_required()]

    @blp.arguments(OrderReturnDetailQueryArgSchema, location='query')
    @blp.response(ReOrderReturnDetailListSchema)
    def get(self, args: dict):
        """查询退货商品明细列表"""
        if "return_id" in args:
            return dict(
                data=order_return_detail_service.get_return_details(args["return_id"]),
                code=200
            )
        # 其他查询条件
        data, total = order_return_detail_service.list(**args)
        return dict(data=data, code=200, total=total)


@blp.route('/shop-order-return-detail/product/<int:product_id>')
class ProductReturnDetailsAPI(MethodView):
    """商品退货记录API"""
    decorators = [auth_required()]

    @blp.response(ReOrderReturnDetailListSchema)
    def get(self, product_id: int):
        """获取指定商品的所有退货记录"""
        return order_return_detail_service.get_product_returns(product_id)


@blp.route('/shop-order-return-log')
class OrderReturnLogAPI(MethodView):
    """退货日志API"""
    decorators = [auth_required()]

    @blp.arguments(OrderReturnLogQueryArgSchema, location='query')
    @blp.response(ReOrderReturnLogListSchema)
    def get(self, args: dict):
        """查询退货日志列表"""
        data, total = order_return_log_service.list(**args)
        return dict(data=data, code=200, total=total)


@blp.route('/shop-order-return-log/return/<int:return_id>')
class ReturnLogsAPI(MethodView):
    """退货单日志API"""
    decorators = [auth_required()]

    @blp.response(ReOrderReturnLogListSchema)
    def get(self, return_id: int):
        """获取指定退货单的所有日志"""
        return dict(
            data=order_return_log_service.get_return_logs(return_id),
            code=200
        )


@blp.route('/shop-order-return-log/return-no/<string:return_no>')
class ReturnLogsByNoAPI(MethodView):
    """通过退货单号查询日志API"""
    decorators = [auth_required()]

    @blp.response(ReOrderReturnLogListSchema)
    def get(self, return_no: str):
        """通过退货单号获取所有日志"""
        return order_return_log_service.get_return_logs_by_no(return_no)


@blp.route('/shop-order-return-log/operator/<string:operator>')
class OperatorReturnLogsAPI(MethodView):
    """操作员退货日志API"""
    decorators = [auth_required()]

    @blp.response(ReOrderReturnLogListSchema)
    def get(self, operator: str):
        """获取指定操作员的所有退货操作日志"""
        return order_return_log_service.get_operator_logs(operator)
