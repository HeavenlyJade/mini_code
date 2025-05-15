from flask.views import MethodView

from backend.mini_core.schema.order.shop_order_logistics import (
    ShopOrderLogisticsQueryArgSchema, ShopOrderLogisticsResponseSchema,
    ShopOrderLogisticsListResponseSchema, ShopOrderLogisticsCreateSchema,
    ShopOrderLogisticsUpdateSchema, LogisticsStatusUpdateSchema,
    LogisticsShipSchema, LogisticsDeliveredSchema, LogisticsDetailResponseSchema,
    LogisticsDateRangeQueryArgSchema, LogisticsStatsResponseSchema
)
from backend.mini_core.service import shop_order_logistics_service
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


@blp.route('/by-order-no/<string:order_no>')
class LogisticsByOrderNoAPI(MethodView):
    """通过订单编号查询物流API"""
    decorators = [auth_required()]

    @blp.response(LogisticsDetailResponseSchema)
    def get(self, order_no: str):
        """通过订单编号获取物流信息"""
        return shop_order_logistics_service.get_logistics_by_order_no(order_no)
