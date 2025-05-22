from backend.mini_core.api.v1 import mini_core_v1_blp, mini_wx_app_v1_blp
from backend.mini_core.api.v1.card import blp as card_api
from backend.mini_core.api.v1.distribution import blp as distribution_api
from backend.mini_core.api.v1.shop import blp as shop_api
from backend.mini_core.api.v1.store import blp as store_api
from backend.mini_core.api.v1.store_category import blp as store_category_api
from backend.mini_core.api.v1.base_server import blp as base_server_api
from backend.mini_core.api.v1.shop_specification import blp as shop_specification_api
from backend.mini_core.api.v1.order import blp as order_api
from backend.mini_core.api.v1.shop_order_detail import blp as shop_order_detail_api
from backend.mini_core.api.v1.order_log import blp as order_log_api
from backend.mini_core.api.v1.shop_order_setting import blp as shop_order_setting_api
from backend.mini_core.api.v1.shop_return_reason import blp as shop_return_reason_api
from backend.mini_core.api.v1.shop_user import blp as shop_user_blp
from backend.mini_core.api.v1.shop_user_address import blp as shop_user_address_blp
from backend.mini_core.api.v1.shop_order_return import blp as shop_order_return_api
from backend.mini_core.api.v1.banner import blp as banner_api
from backend.mini_core.api.v1.shop_order_logistics import blp as shop_order_logistics_api
from backend.mini_core.api.v1.shop_order_review import  blp as order_review_blp
from backend.mini_core.api.v1.dashboard import blp as dashboard_api


mini_core_v1_blp.register_blueprint(card_api)
mini_core_v1_blp.register_blueprint(distribution_api)
mini_core_v1_blp.register_blueprint(shop_api)
mini_core_v1_blp.register_blueprint(store_api)
mini_core_v1_blp.register_blueprint(store_category_api)
mini_core_v1_blp.register_blueprint(base_server_api)
mini_core_v1_blp.register_blueprint(shop_specification_api)
mini_core_v1_blp.register_blueprint(order_api)
mini_core_v1_blp.register_blueprint(shop_order_detail_api)
mini_core_v1_blp.register_blueprint(order_log_api)
mini_core_v1_blp.register_blueprint(shop_order_setting_api)
mini_core_v1_blp.register_blueprint(shop_return_reason_api)
mini_core_v1_blp.register_blueprint(shop_user_blp)
mini_core_v1_blp.register_blueprint(shop_user_address_blp)
mini_core_v1_blp.register_blueprint(shop_order_return_api)
mini_core_v1_blp.register_blueprint(banner_api)
mini_core_v1_blp.register_blueprint(shop_order_logistics_api)
mini_core_v1_blp.register_blueprint(order_review_blp)
mini_core_v1_blp.register_blueprint(dashboard_api)


from backend.mini_core.api.v1.mini_api.shop_user import blp as wx_shop_user_api
from backend.mini_core.api.v1.mini_api.banner import blp as ws_banner_api_banner
from backend.mini_core.api.v1.mini_api.app_user import blp as wx_app_user_api
from backend.mini_core.api.v1.mini_api.app_shop import blp as wx_app_shop_api
from backend.mini_core.api.v1.mini_api.shop_order_cart import blp as cart_api
from backend.mini_core.api.v1.mini_api.wx_shop_order import blp as wx_shop_order_api
from backend.mini_core.api.v1.mini_api.wx_distribution import blp as wx_distribution_api
from backend.mini_core.api.v1.mini_api.app_store import blp as app_store_api
from backend.mini_core.api.v1.mini_api.wx_pay import blp as wx_pay_api
from backend.mini_core.api.v1.mini_api.app_order_logistics import blp as app_order_logistics_api
from backend.mini_core.api.v1.mini_api.shop import blp as shop_api
from backend.mini_core.api.v1.mini_api.shop_return_reason import blp as wx_shop_return_reason_api
mini_wx_app_v1_blp.register_blueprint(wx_shop_user_api)
mini_wx_app_v1_blp.register_blueprint(base_server_api)
mini_wx_app_v1_blp.register_blueprint(ws_banner_api_banner)
mini_wx_app_v1_blp.register_blueprint(wx_app_user_api)
mini_wx_app_v1_blp.register_blueprint(wx_app_shop_api)
mini_wx_app_v1_blp.register_blueprint(shop_api)
mini_wx_app_v1_blp.register_blueprint(cart_api)
mini_wx_app_v1_blp.register_blueprint(wx_shop_order_api)
mini_wx_app_v1_blp.register_blueprint(wx_distribution_api)
mini_wx_app_v1_blp.register_blueprint(app_store_api)
mini_wx_app_v1_blp.register_blueprint(wx_pay_api)
mini_wx_app_v1_blp.register_blueprint(app_order_logistics_api)
mini_wx_app_v1_blp.register_blueprint(wx_shop_return_reason_api)


