from flask.views import MethodView
from flask import current_app

from backend.mini_core.schema.order.order import (
    ShopOrderQueryArgSchema, ReShopOrderSchema, ReShopOrderListSchema,
    OrderStatusUpdateArgSchema, PaymentStatusUpdateArgSchema,
    DeliveryStatusUpdateArgSchema, RefundStatusUpdateArgSchema,
    OrderCreateSchema, DateRangeQueryArgSchema,
    ReOrderStatsSchema, ReMonthlySalesSchema,ShippingInfoUpdateArgSchema
)
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_order_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_order', 'shop_order', url_prefix='/')


@blp.route('/shop-order')
class ShopOrderAPI(MethodView):
    """订单API"""
    decorators = [auth_required()]

    @blp.arguments(ShopOrderQueryArgSchema, location='query')
    @blp.response(ReShopOrderListSchema)
    def get(self, args: dict):
        """查询订单列表"""
        return shop_order_service.get_order_list(args)

    # @blp.arguments(OrderCreateSchema)
    # @blp.response(ReShopOrderSchema)
    # def post(self, order_data):
    #     """创建订单"""
    #     return shop_order_service.create_order(order_data)


@blp.route('/shop-order/<int:order_id>')
class ShopOrderDetailAPI(MethodView):
    """订单详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def get(self, order_id: int):
        """获取指定ID的订单"""
        return shop_order_service.get_order_by_id(order_id)

    @blp.arguments(ShopOrderQueryArgSchema)
    @blp.response(ReShopOrderSchema)
    def put(self, order_data, order_id: int):
        """更新指定ID的订单"""
        return shop_order_service.update(order_id, order_data)

    @blp.response(ReShopOrderSchema)
    def delete(self, order_id: int):
        """删除指定ID的订单"""
        return shop_order_service.delete(order_id)


@blp.route('/shop-order/by-order-no/<string:order_no>')
class ShopOrderByOrderNoAPI(MethodView):
    """通过订单编号查询订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def get(self, order_no: str):
        """通过订单编号获取订单信息"""
        return shop_order_service.get_order_by_order_no(order_no)


@blp.route('/shop-order/by-order-sn/<string:order_sn>')
class ShopOrderByOrderSnAPI(MethodView):
    """通过订单号查询订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def get(self, order_sn: str):
        """通过订单号获取订单信息"""
        return shop_order_service.get_order_by_order_sn(order_sn)


@blp.route('/shop-order/user/<int:user_id>')
class UserOrdersAPI(MethodView):
    """用户订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderListSchema)
    def get(self, user_id: int):
        """获取用户的所有订单"""
        return shop_order_service.get_user_orders(user_id)


@blp.route('/shop-order/stats')
class OrderStatsAPI(MethodView):
    """订单统计API"""
    decorators = [auth_required()]

    @blp.response(ReOrderStatsSchema)
    def get(self):
        """获取订单统计信息"""
        return shop_order_service.get_order_stats()


@blp.route('/shop-order/monthly-sales')
class MonthlySalesAPI(MethodView):
    """月度销售统计API"""
    decorators = [auth_required()]

    @blp.arguments(DateRangeQueryArgSchema, location='query')
    @blp.response(ReMonthlySalesSchema)
    def get(self, args: dict):
        """获取月度销售统计"""
        return shop_order_service.get_monthly_sales()


@blp.route('/shop-order/status')
class OrderStatusAPI(MethodView):
    """订单状态API"""
    decorators = [auth_required()]

    @blp.arguments(OrderStatusUpdateArgSchema)
    @blp.response(ReShopOrderSchema)
    def post(self, args):
        """更新订单状态"""
        return shop_order_service.update_order_status(args["id"], args["status"])


@blp.route('/shop-order/payment-status')
class PaymentStatusAPI(MethodView):
    """支付状态API"""
    decorators = [auth_required()]

    @blp.arguments(PaymentStatusUpdateArgSchema)
    @blp.response(ReShopOrderSchema)
    def post(self, args):
        """更新支付状态"""
        return shop_order_service.update_payment_status(
            args["id"],
            args["payment_status"],
            args.get("payment_no"),
            args.get("trade_no")
        )


@blp.route('/shop-order/refund-status')
class RefundStatusAPI(MethodView):
    """退款状态API"""
    decorators = [auth_required()]

    @blp.arguments(RefundStatusUpdateArgSchema)
    @blp.response(ReShopOrderSchema)
    def post(self, args):
        """更新退款状态"""
        return shop_order_service.update_refund_status(args["id"], args["refund_status"])


@blp.route('/shop-order/cancel/<int:order_id>')
class CancelOrderAPI(MethodView):
    """取消订单API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def post(self, order_id: int):
        """取消订单"""
        return shop_order_service.cancel_order(order_id)


@blp.route('/shop-order/confirm-receipt/<int:order_id>')
class ConfirmReceiptAPI(MethodView):
    """确认收货API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSchema)
    def post(self, order_id: int):
        """确认收货"""
        return shop_order_service.confirm_receipt(order_id)


# @blp.route('/shop-order/close/<int:order_id>')
# class CloseOrderAPI(MethodView):
#     """关闭订单API"""
#     decorators = [auth_required()]
#
#     @blp.response(ReShopOrderSchema)
#     def post(self, order_id: int):
#         """关闭订单"""
#         return shop_order_service.close_order(order_id)

@blp.route('/shop-order/shipping-info')
class OrderShippingInfoAPI(MethodView):
    """订单物流信息API"""
    decorators = [auth_required()]

    @blp.arguments(ShippingInfoUpdateArgSchema)
    @blp.response(ReShopOrderSchema)
    def post(self, args):
        """更新订单物流信息"""
        return shop_order_service.update_shipping_info(args["order_no"],args)
