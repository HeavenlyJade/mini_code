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


@blp.route('/')
class ShopOrderLogisticsAPI(MethodView):
    """订单物流管理API"""
    decorators = [auth_required()]

    @blp.arguments(ShopOrderLogisticsQueryArgSchema, location='query')
    @blp.response(ShopOrderLogisticsListResponseSchema)
    def get(self, args: dict):
        """查询物流信息列表"""
        return shop_order_logistics_service.get_logistics_list(args)

    @blp.arguments(ShopOrderLogisticsCreateSchema)
    @blp.response(ShopOrderLogisticsResponseSchema)
    def post(self, logistics_data):
        """创建物流信息"""
        return shop_order_logistics_service.create_logistics(logistics_data)


@blp.route('/<int:logistics_id>')
class ShopOrderLogisticsDetailAPI(MethodView):
    """订单物流详情API"""
    decorators = [auth_required()]

    @blp.response(LogisticsDetailResponseSchema)
    def get(self, logistics_id: int):
        """获取指定ID的物流信息"""
        return shop_order_logistics_service.get_logistics_by_id(logistics_id)

    @blp.arguments(ShopOrderLogisticsUpdateSchema)
    @blp.response(ShopOrderLogisticsResponseSchema)
    def put(self, logistics_data, logistics_id: int):
        """更新指定ID的物流信息"""
        return shop_order_logistics_service.update_logistics(logistics_id, logistics_data)

    @blp.response(ShopOrderLogisticsResponseSchema)
    def delete(self, logistics_id: int):
        """删除指定ID的物流信息"""
        return shop_order_logistics_service.delete_logistics(logistics_id)


@blp.route('/by-order-no/<string:order_no>')
class LogisticsByOrderNoAPI(MethodView):
    """通过订单编号查询物流API"""
    decorators = [auth_required()]

    @blp.response(LogisticsDetailResponseSchema)
    def get(self, order_no: str):
        """通过订单编号获取物流信息"""
        return shop_order_logistics_service.get_logistics_by_order_no(order_no)
@blp.route('/by-logistics-no/<string:logistics_no>')
class LogisticsByLogisticsNoAPI(MethodView):
    """通过物流单号查询物流API"""
    decorators = [auth_required()]

    @blp.response(LogisticsDetailResponseSchema)
    def get(self, logistics_no: str):
        """通过物流单号获取物流信息"""
        return shop_order_logistics_service.get_logistics_by_logistics_no(logistics_no)


