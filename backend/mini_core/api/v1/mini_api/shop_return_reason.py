from flask.views import MethodView

from backend.mini_core.schema.order.shop_return_reason import (
    ShopReturnReasonQueryArgSchema,  ReShopReturnReasonListSchema,

)
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_return_reason_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_return_reason', 'shop_return_reason', url_prefix='/shop-return-reason')


@blp.route('/')
class ShopReturnReasonAPI(MethodView):
    """退货原因API"""
    decorators = [auth_required()]

    @blp.arguments(ShopReturnReasonQueryArgSchema,)
    @blp.response(ReShopReturnReasonListSchema)
    def post(self, args: dict):
        """查询退货原因列表"""
        return shop_return_reason_service.get_reasons(args)

