from flask.views import MethodView

from backend.mini_core.schema.order.shop_order_cart import (
    ShopOrderCartQueryArgSchema, ShopOrderCartResponseSchema, ShopOrderCartListResponseSchema,
    CartItemAddSchema, CartItemUpdateSchema, CartItemDeleteSchema, CartItemWithProductListResponseSchema
)
from backend.mini_core.service import shop_order_cart_service
from backend.business.service.auth import auth_required
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_order_cart', 'shop_order_cart', url_prefix='/')


@blp.route('/shop-cart')
class ShopOrderCartAPI(MethodView):
    """购物车API"""
    decorators = [auth_required()]

    # @blp.arguments(ShopOrderCartQueryArgSchema, location='query')
    @blp.response()
    def get(self, ):
        """获取用户购物车"""
        return shop_order_cart_service.get_user_cart()

    @blp.arguments(CartItemAddSchema)
    @blp.response(ShopOrderCartResponseSchema)
    def post(self, cart_item):
        """添加商品到购物车"""
        print(cart_item)
        return shop_order_cart_service.add_to_cart(cart_item)


@blp.route('/shop-cart/update')
class ShopOrderCartUpdateAPI(MethodView):
    """购物车更新API"""
    decorators = [auth_required()]

    @blp.arguments(CartItemUpdateSchema)
    @blp.response(ShopOrderCartResponseSchema)
    def post(self, args):
        """更新购物车商品数量"""
        return shop_order_cart_service.update_cart_item(args)


@blp.route('/shop-cart/delete')
class ShopOrderCartDeleteAPI(MethodView):
    """购物车删除API"""
    decorators = [auth_required()]

    @blp.arguments(CartItemDeleteSchema)
    @blp.response(ShopOrderCartResponseSchema)
    def post(self, args):
        """从购物车中删除商品"""
        return shop_order_cart_service.delete_cart_item(args['sku_id'])


@blp.route('/shop-cart/clear/<string:user_id>')
class ShopOrderCartClearAPI(MethodView):
    """清空购物车API"""
    decorators = [auth_required()]

    @blp.response(ShopOrderCartResponseSchema)
    def post(self, user_id: str):
        """清空用户购物车"""
        return shop_order_cart_service.clear_cart(user_id)


@blp.route('/shop-cart/count/<string:user_id>')
class ShopOrderCartCountAPI(MethodView):
    """购物车商品数量API"""
    decorators = [auth_required()]

    @blp.response()
    def get(self, user_id: str):
        """获取用户购物车商品总数"""
        return shop_order_cart_service.get_cart_count(user_id)


@blp.route('/shop-cart/batch-add')
class ShopOrderCartBatchAddAPI(MethodView):
    """批量添加购物车API"""
    decorators = [auth_required()]

    @blp.arguments(CartItemAddSchema(many=True))
    @blp.response(ShopOrderCartResponseSchema)
    def post(self, items):
        """批量添加商品到购物车"""
        results = []
        for item in items:
            result = shop_order_cart_service.add_to_cart(item)
            results.append(result)

        return {'code': 200, 'message': '批量添加完成', 'data': results}
