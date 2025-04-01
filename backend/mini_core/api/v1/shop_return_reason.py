from flask.views import MethodView

from backend.mini_core.schema.order.shop_return_reason import (
    ShopReturnReasonQueryArgSchema, ReShopReturnReasonSchema, ReShopReturnReasonListSchema,
    ReturnReasonStatusUpdateArgSchema, ReturnReasonSortUpdateArgSchema, DeleteIdsSchema,
    ShopReturnReasonSchema
)
from backend.mini_core.domain.order.shop_return_reason import ShopReturnReason
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_return_reason_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_return_reason', 'shop_return_reason', url_prefix='/')


@blp.route('/shop-return-reason')
class ShopReturnReasonAPI(MethodView):
    """退货原因API"""
    decorators = [auth_required()]

    @blp.arguments(ShopReturnReasonQueryArgSchema, location='query')
    @blp.response(ReShopReturnReasonListSchema)
    def get(self, args: dict):
        """查询退货原因列表"""
        return shop_return_reason_service.get_reasons(args)

    @blp.arguments(ShopReturnReasonSchema)
    @blp.response(ReShopReturnReasonSchema)
    def post(self, reason):
        """创建退货原因"""
        return shop_return_reason_service.create_reason(reason)


@blp.route('/shop-return-reason/enabled')
class ShopReturnReasonEnabledAPI(MethodView):
    """获取启用的退货原因API"""

    @blp.response(ReShopReturnReasonListSchema)
    def get(self):
        """获取所有启用的退货原因"""
        return shop_return_reason_service.get_enabled_reasons()


@blp.route('/shop-return-reason/<int:reason_id>')
class ShopReturnReasonDetailAPI(MethodView):
    """退货原因详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopReturnReasonSchema)
    def get(self, reason_id: int):
        """获取指定ID的退货原因"""
        return shop_return_reason_service.get_by_id(reason_id)

    @blp.arguments(ShopReturnReasonSchema)
    @blp.response(ReShopReturnReasonSchema)
    def put(self, reason, reason_id: int):
        """更新指定ID的退货原因"""
        return shop_return_reason_service.update_reason(reason_id, reason)

    @blp.response(ReShopReturnReasonSchema)
    def delete(self, reason_id: int):
        """删除指定ID的退货原因"""
        return shop_return_reason_service.delete_reason(reason_id)


@blp.route('/shop-return-reason/batch-delete')
class ShopReturnReasonBatchDeleteAPI(MethodView):
    """批量删除退货原因API"""
    decorators = [auth_required()]

    @blp.arguments(DeleteIdsSchema)
    @blp.response(ReShopReturnReasonSchema)
    def post(self, args):
        """批量删除退货原因"""
        return shop_return_reason_service.batch_delete(args["ids"])


@blp.route('/shop-return-reason/status')
class ShopReturnReasonStatusAPI(MethodView):
    """退货原因状态API"""
    decorators = [auth_required()]

    @blp.arguments(ReturnReasonStatusUpdateArgSchema)
    @blp.response(ReShopReturnReasonSchema)
    def post(self, args):
        """更新退货原因状态"""
        return shop_return_reason_service.update_status(args["id"], args["is_enabled"])


@blp.route('/shop-return-reason/sort')
class ShopReturnReasonSortAPI(MethodView):
    """退货原因排序API"""
    decorators = [auth_required()]

    @blp.arguments(ReturnReasonSortUpdateArgSchema)
    @blp.response(ReShopReturnReasonSchema)
    def post(self, args):
        """更新退货原因排序"""
        return shop_return_reason_service.update_sort_order(args["id"], args["sort_order"])
