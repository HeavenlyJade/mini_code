from flask.views import MethodView

from backend.mini_core.schema.order.order import (
    ShopOrderQueryArgSchema, ReShopOrderSchema, ReShopOrderListSchema,
    OrderStatusUpdateArgSchema, PaymentStatusUpdateArgSchema,
    DeliveryStatusUpdateArgSchema,
    OrderCreateSchema, DateRangeQueryArgSchema, WXShopOrderQueryArgSchema,
    ReOrderStatsSchema, ReMonthlySalesSchema, MiniOrderCreateSchema
)
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_order_service
from kit.util.blueprint import APIBlueprint

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


@blp.route('/order_status_data')
class ShopOrderListAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(WXShopOrderQueryArgSchema)
    @blp.response()
    def post(self, order_data):
        """ 订单退货"""
        status = order_data["status"]
        order_data["status"] = status.split(",")
        return shop_order_service.get_order_detail_msg(order_data)

    @blp.arguments(WXShopOrderQueryArgSchema)
    @blp.response()
    def put(self, order_data):
        return shop_order_service.update_refund_status(order_data)


@blp.route('/<int:order_id>')
class ShopOrderDetailAPI(MethodView):
    """订单详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def get(self, order_id: int):
        """获取指定ID的订单"""
        return shop_order_service.get_order_by_id(order_id)


@blp.route('/by-order-no/<string:order_no>')
class ShopOrderByOrderNoAPI(MethodView):
    """通过订单编号查询订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def get(self, order_no: str):
        """通过订单编号获取订单信息"""
        return shop_order_service.get_order_by_order_no(order_no)


@blp.route('/by-order-sn/<string:order_sn>')
class ShopOrderByOrderSnAPI(MethodView):
    """通过订单号查询订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def get(self, order_sn: str):
        """通过订单号获取订单信息"""
        return shop_order_service.get_order_by_order_sn(order_sn)


@blp.route('/user/<int:user_id>')
class UserOrdersAPI(MethodView):
    """用户订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderListSchema)
    def get(self, user_id: int):
        """获取用户的所有订单"""
        return shop_order_service.get_user_orders(user_id)


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
