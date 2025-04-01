from flask.views import MethodView

from backend.mini_core.schema.order.order_detail import (
    OrderDetailQueryArgSchema, OrderDetailResponseSchema, OrderDetailListResponseSchema,
    OrderDetailCreateSchema, BatchCreateOrderDetailSchema
)
from backend.mini_core.service import order_detail_service
from backend.business.service.auth import auth_required
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('order_detail', 'order_detail', url_prefix='/')


@blp.route('/order-details')
class OrderDetailAPI(MethodView):
    """订单详情API"""
    decorators = [auth_required()]

    @blp.arguments(OrderDetailQueryArgSchema, location='query')
    # @blp.response(OrderDetailListResponseSchema)
    def get(self, args: dict):
        """查询订单详情列表"""
        return order_detail_service.get_order_details(args)

    @blp.arguments(OrderDetailCreateSchema)
    @blp.response(OrderDetailResponseSchema)
    def post(self, detail):
        """创建订单详情"""
        return order_detail_service.create_order_detail(detail)


@blp.route('/order-details/batch')
class OrderDetailBatchAPI(MethodView):
    """批量订单详情API"""
    decorators = [auth_required()]

    @blp.arguments(BatchCreateOrderDetailSchema)
    def post(self, args):
        """批量创建订单详情"""
        return order_detail_service.batch_create_details(args["items"])


@blp.route('/order-details/<int:detail_id>')
class OrderDetailByIDAPI(MethodView):
    """订单详情管理API"""
    decorators = [auth_required()]

    @blp.response(OrderDetailResponseSchema)
    def get(self, detail_id: int):
        """获取指定ID的订单详情"""
        return dict(data=order_detail_service.get(detail_id), code=200)

    @blp.arguments(OrderDetailCreateSchema)
    @blp.response(OrderDetailResponseSchema)
    def put(self, detail, detail_id: int):
        """更新指定ID的订单详情"""
        return order_detail_service.update_detail(detail_id, detail)

    @blp.response()
    def delete(self, detail_id: int):
        """删除指定ID的订单详情"""
        return order_detail_service.delete_detail(detail_id)


@blp.route('/orders/<string:order_no>/details')
class OrderDetailsByOrderAPI(MethodView):
    """订单的详情API"""
    decorators = [auth_required()]

    @blp.response(OrderDetailListResponseSchema)
    def get(self, order_no: str):
        """获取指定订单的所有详情"""
        return order_detail_service.get_order_details(order_no)


@blp.route('/orders/<string:order_no>/gifts')
class OrderGiftsByOrderAPI(MethodView):
    """订单赠品API"""
    decorators = [auth_required()]

    @blp.response(OrderDetailListResponseSchema)
    def get(self, order_no: str):
        """获取指定订单的所有赠品详情"""
        return order_detail_service.get_gift_details(order_no)


@blp.route('/orders/<string:order_no>/amount')
class OrderAmountAPI(MethodView):
    """订单金额计算API"""
    decorators = [auth_required()]

    @blp.response()
    def get(self, order_no: str):
        """计算订单总金额信息"""
        return order_detail_service.get_order_amount(order_no)


@blp.route('/products/<int:product_id>/orders')
class ProductOrdersAPI(MethodView):
    """商品订单API"""
    decorators = [auth_required()]

    @blp.response(OrderDetailListResponseSchema)
    def get(self, product_id: int):
        """获取指定商品的所有订单详情"""
        return order_detail_service.get_product_orders(product_id)
