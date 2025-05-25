from flask.views import MethodView

from backend.mini_core.schema.order.order import (ReShopOrderSchema, OrderStatusUpdateArgSchema,
                                                  WXShopOrderQueryArgSchema, MiniOrderCreateSchema)

from backend.mini_core.schema.order.order_return import (
    OrderReturnQueryArgSchema, ReOrderReturnSchema, ReOrderReturnListSchema,AuditReturnSchema,
    ReturnApplicationSchema)
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_order_service, order_return_service
from kit.util.blueprint import APIBlueprint
from flask_jwt_extended import get_current_user

blp = APIBlueprint('wx_shop_order', 'wx_shop_order', url_prefix='/shop-order')


@blp.route('/')
class ShopOrderAPI(MethodView):
    """订单API"""
    decorators = [auth_required()]

    @blp.arguments(WXShopOrderQueryArgSchema, location='query')
    @blp.response()
    def get(self, args: dict):
        """查询订单列表"""
        return shop_order_service.get_order_detail_msg(args)

    @blp.arguments(MiniOrderCreateSchema)
    @blp.response(ReShopOrderSchema)
    def post(self, order_data):
        """创建订单"""
        return shop_order_service.create_order(order_data)


@blp.route('/status')
class OrderStatusAPI(MethodView):
    """订单状态API"""
    decorators = [auth_required()]

    @blp.arguments(OrderStatusUpdateArgSchema)
    @blp.response(ReShopOrderSchema)
    def post(self, args):
        """更新订单状态"""
        return shop_order_service.update_order_status(args["order_no"], args["status"])


@blp.route('/cancel/')
class CancelOrderAPI(MethodView):
    """取消订单API"""
    decorators = [auth_required()]

    @blp.arguments(OrderStatusUpdateArgSchema)
    @blp.response(ReShopOrderSchema)
    def post(self, args: dict):
        """取消订单"""
        return shop_order_service.cancel_order(args)


@blp.route('/payment/<int:order_id>')
class PaymentReceiptAPI(MethodView):
    """付款确认的api"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def post(self, order_id: int):
        """确认付款"""
        return shop_order_service.change_order_to_paid(order_id)


@blp.route('/by-order-no/<string:order_no>')
class ShopOrderByOrderNoAPI(MethodView):
    """通过订单编号查询订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def get(self, order_no: str):
        """通过订单编号获取订单信息"""
        return shop_order_service.get_order_by_order_no(order_no)


@blp.route('/order-return-data')
class ShopOrderListAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(WXShopOrderQueryArgSchema)
    @blp.response()
    def post(self, args: dict):
        """查询退货单列表"""
        return order_return_service.get_return_order_messages(args)


@blp.route('/shop-order-return')
class OrderReturnAPI(MethodView):
    """订单退货API"""
    decorators = [auth_required()]

    @blp.arguments(ReturnApplicationSchema)
    @blp.response()
    def post(self, application):
        """创建退货申请"""
        return order_return_service.create_return(application)


# @blp.route('/shop-order-return/<string:order_no>/audit')
# class AuditOrderReturnAPI(MethodView):
#     """审核退货单API"""
#     decorators = [auth_required()]
#
#     @blp.arguments(AuditReturnSchema)
#     @blp.response(ReOrderReturnSchema)
#     def put(self, args, order_no: str):
#         """审核退货单"""
#         status = args.pop("status")
#         return order_return_service.update_return_status(order_no, status, **args)
