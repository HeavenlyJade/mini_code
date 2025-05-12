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


@blp.route('/<int:logistics_id>/status')
class LogisticsStatusAPI(MethodView):
    """物流状态管理API"""
    decorators = [auth_required()]

    @blp.arguments(LogisticsStatusUpdateSchema)
    @blp.response(ShopOrderLogisticsResponseSchema)
    def post(self, args, logistics_id: int):
        """更新物流状态"""
        return shop_order_logistics_service.update_logistics_status(
            logistics_id,
            args['status'],
            args.get('location')
        )


@blp.route('/<int:logistics_id>/ship')
class LogisticsShipAPI(MethodView):
    """物流发货API"""
    decorators = [auth_required()]

    @blp.arguments(LogisticsShipSchema)
    @blp.response(ShopOrderLogisticsResponseSchema)
    def post(self, args, logistics_id: int):
        """标记物流为已发货"""
        # 先更新物流信息
        update_data = {
            'logistics_company': args['logistics_company'],
            'logistics_no': args['logistics_no']
        }

        if 'courier_number' in args:
            update_data['courier_number'] = args['courier_number']

        if 'courier_phone' in args:
            update_data['courier_phone'] = args['courier_phone']

        if 'current_location' in args:
            update_data['current_location'] = args['current_location']

        if 'remark' in args:
            update_data['remark'] = args['remark']

        shop_order_logistics_service.update_logistics(logistics_id, update_data)

        # 然后标记为已发货
        return shop_order_logistics_service.mark_as_shipped(
            logistics_id,
            args.get('shipping_time')
        )


@blp.route('/<int:logistics_id>/deliver')
class LogisticsDeliverAPI(MethodView):
    """物流送达API"""
    decorators = [auth_required()]

    @blp.arguments(LogisticsDeliveredSchema)
    @blp.response(ShopOrderLogisticsResponseSchema)
    def post(self, args, logistics_id: int):
        """标记物流为已送达"""
        return shop_order_logistics_service.mark_as_delivered(
            logistics_id,
            args.get('receiving_time')
        )


@blp.route('/active')
class ActiveLogisticsAPI(MethodView):
    """活跃物流API"""
    decorators = [auth_required()]

    @blp.response(ShopOrderLogisticsListResponseSchema)
    def get(self):
        """获取所有活跃的物流信息（尚未送达的）"""
        return shop_order_logistics_service.get_active_logistics()


@blp.route('/date-range')
class LogisticsDateRangeAPI(MethodView):
    """日期范围物流查询API"""
    decorators = [auth_required()]

    @blp.arguments(LogisticsDateRangeQueryArgSchema, location='query')
    @blp.response(ShopOrderLogisticsListResponseSchema)
    def get(self, args):
        """获取指定日期范围内的物流信息"""
        return shop_order_logistics_service.get_logistics_by_date_range(
            args['start_date'],
            args['end_date']
        )


@blp.route('/stats')
class LogisticsStatsAPI(MethodView):
    """物流统计API"""
    decorators = [auth_required()]

    @blp.response(LogisticsStatsResponseSchema)
    def get(self):
        """获取物流统计信息"""
        # 获取所有物流信息
        all_logistics = shop_order_logistics_service._repo.find_all()

        # 计算活跃和已送达数量
        active_count = 0
        delivered_count = 0
        status_stats = {}

        for logistics in all_logistics:
            if logistics.current_status not in status_stats:
                status_stats[logistics.current_status] = 0
            status_stats[logistics.current_status] += 1

            if logistics.receiving_time is None:
                active_count += 1
            else:
                delivered_count += 1

        # 转换为列表格式
        status_stats_list = [{'status': status, 'count': count} for status, count in status_stats.items()]

        return {
            'data': {
                'total': len(all_logistics),
                'active': active_count,
                'delivered': delivered_count,
                'status_stats': status_stats_list
            },
            'code': 200
        }
