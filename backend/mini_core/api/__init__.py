from backend.mini_core.api.v1 import mini_core_v1_blp
from backend.mini_core.api.v1.card import blp as card_api
from backend.mini_core.api.v1.distribution import blp as distribution_api
from backend.mini_core.api.v1.shop import blp as shop_api
from backend.mini_core.api.v1.store import blp as store_api
from backend.mini_core.api.v1.store_category import blp as store_category_api
from backend.mini_core.api.v1.base_server import blp as base_server_api
mini_core_v1_blp.register_blueprint(card_api)
mini_core_v1_blp.register_blueprint(distribution_api)
mini_core_v1_blp.register_blueprint(shop_api)
mini_core_v1_blp.register_blueprint(store_api)
mini_core_v1_blp.register_blueprint(store_category_api)
mini_core_v1_blp.register_blueprint(base_server_api)




