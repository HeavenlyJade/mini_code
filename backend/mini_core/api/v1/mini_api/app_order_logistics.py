from flask.views import MethodView

from backend.mini_core.schema.order.shop_order_logistics import (
    LogisticsQuerySchema, LogisticsDetailResponseSchema,
)
from backend.mini_core.schema.order.order import ( ReShopOrderSchema,OrderStatusUpdateArgSchema)
from backend.mini_core.service import shop_order_logistics_service
from backend.mini_core.service import shop_order_service

from backend.business.service.auth import auth_required
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_order_logistics', 'shop_order_logistics', url_prefix='/logistics')


@blp.route('/<int:logistics_id>')
class ShopOrderLogisticsDetailAPI(MethodView):
    """订单物流详情API"""
    decorators = [auth_required()]

    @blp.response(LogisticsDetailResponseSchema)
    def get(self, logistics_id: int):
        """获取指定ID的物流信息"""
        return shop_order_logistics_service.get_logistics_by_id(logistics_id)


@blp.route('/by-order-no/')
class LogisticsByOrderNoAPI(MethodView):
    """通过订单编号查询物流API"""
    decorators = [auth_required()]

    @blp.arguments(LogisticsQuerySchema)
    @blp.response(LogisticsDetailResponseSchema)
    def post(self,args:dict):
        """通过订单编号获取物流信息"""
        order_no = args['order_no']
        return shop_order_logistics_service.get_logistics_by_order_no(order_no)
