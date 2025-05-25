from flask.views import MethodView

from backend.mini_core.schema.order.order_return import (
    OrderReturnQueryArgSchema, ReOrderReturnSchema, ReOrderReturnListSchema,

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

    # @blp.arguments(ReturnApplicationSchema)
    # @blp.response(ReOrderReturnSchema)
    # def post(self, application):
    #     """创建退货申请"""
    #     return order_return_service.create_return(application["return_info"], application["return_items"])
    #

@blp.route('/shop-order-return_detail')
class OrderReturnDetailAPI(MethodView):
    """退货单详情API"""
    decorators = [auth_required()]

    @blp.arguments(OrderReturnQueryArgSchema, location='query')
    @blp.response(ReCompleteReturnDetailSchema)
    def get(self, args: dict):
        """获取指定订单号的退货单详情"""
        return order_return_service.get_return_by_order_no(args["order_no"])



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





