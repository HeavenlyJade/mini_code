from flask.views import MethodView
from backend.mini_core.schema.shop import ( ReShopProductSchema)

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

