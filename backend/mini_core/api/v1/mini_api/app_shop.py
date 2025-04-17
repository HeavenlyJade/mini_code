from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    jwt_required
)

from backend.mini_core.domain.t_user import ShopUserAddress
from backend.mini_core.schema.shop_app.wx_login import WechatLoginSchema, ShopAppSchema
from backend.mini_core.schema.shop import ( ReShopProductSchema)
from backend.mini_core.service import shop_user_address_service
from backend.mini_core.service import shop_user_service
from backend.mini_core.service.shop_app import wechat_auth_service
from kit.exceptions import ServiceBadRequest
from kit.util.blueprint import APIBlueprint
from backend.mini_core.service import (shop_product_service)
blp = APIBlueprint('wx_shop', 'wx_shop', url_prefix='/wx_shop')


@blp.route('/shop-product/<int:product_id>')
class ShopProductDetailAPI(MethodView):
    """商品详情API"""

    @blp.response(ReShopProductSchema)
    def get(self, product_id: int):
        """获取指定ID的商品"""
        data = shop_product_service.get({"id": product_id})
        return dict(code=200,data=data)

