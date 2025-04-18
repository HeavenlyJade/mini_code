from flask.views import MethodView

from backend.mini_core.schema.order.shop_order_cart import (
    ShopOrderCartQueryArgSchema, ShopOrderCartResponseSchema, ShopOrderCartListResponseSchema,
    CartItemAddSchema, CartItemUpdateSchema, CartItemDeleteSchema, CartItemWithProductListResponseSchema
)
from backend.mini_core.service import shop_order_cart_service
from backend.business.service.auth import auth_required
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_pay', 'shop_pay', url_prefix='/shop_pay')
