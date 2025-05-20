from flask.views import MethodView

from backend.mini_core.schema.store.store import (
    ShopStoreQueryArgSchema, ReShopStoreSchema, ReShopStoreListSchema,
    ShopStoreStatusUpdateArgSchema, NearbyStoreQueryArgSchema, ServiceModeToggleArgSchema,
    BusinessHoursUpdateArgSchema, DeliverySettingsUpdateArgSchema, ContactInfoUpdateArgSchema,
    WifiSettingsUpdateArgSchema, ReShopStoreStatsSchema, ReNearbyStoreListSchema,KeywordSearchSchema,
    ShopStoreSchema
)
from backend.mini_core.schema.banner import (BannerIDSchema)
from backend.mini_core.domain.store import ShopStore
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_store_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_store', 'shop_store', url_prefix='/')


@blp.route('/base_down')
class BaseDownAPI(MethodView):
    """基础下载API"""
    @blp.arguments(KeywordSearchSchema, location='query')
    def get(self,args: dict):
        """获取基础下载内容"""
        return shop_store_service.get_table_down_data(args)

@blp.route('/shop-store')
class ShopStoreAPI(MethodView):
    """商店API"""
    decorators = [auth_required()]

    @blp.arguments(ShopStoreQueryArgSchema, location='query')
    # @blp.response(ReShopStoreListSchema)
    def get(self, args: dict):
        """查询商店列表"""
        return shop_store_service.get_store(args)

    @blp.arguments(ShopStoreSchema)
    @blp.response(ReShopStoreSchema)
    def post(self, store):
        """创建或更新商店"""
        if store.id:
            return shop_store_service.update_store(store["id"], store)
        else:
            return shop_store_service.create_store(store)


@blp.route('/shop-store/<int:store_id>')
class ShopStoreDetailAPI(MethodView):
    """商店详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopStoreSchema)
    def get(self, store_id: int):
        """获取指定ID的商店"""
        return shop_store_service.get_by_id(store_id)

    @blp.arguments(ShopStoreSchema)
    @blp.response(ReShopStoreSchema)
    def put(self, store, store_id: int):
        """更新指定ID的商店"""
        return shop_store_service.update_store(store_id, store)

    @blp.response(ReShopStoreSchema)
    def delete(self, store_id: int):
        """删除指定ID的商店"""
        return shop_store_service.delete_store(store_id)


@blp.route('/shop-store/category/<int:category_id>')
class ShopStoreByCategoryAPI(MethodView):
    """按分类查询商店API"""

    @blp.response(ReShopStoreListSchema)
    def get(self, category_id: int):
        """获取指定分类下的所有商店"""
        return shop_store_service.get_by_category(category_id)


@blp.route('/shop-store/search')
class ShopStoreSearchAPI(MethodView):
    """搜索商店API"""

    @blp.arguments(KeywordSearchSchema, location='query')  # 使用 Schema 类
    @blp.response(ReShopStoreListSchema)
    def get(self, args):
        """搜索商店"""
        return shop_store_service.search(args["keyword"])


@blp.route('/shop-store/nearby')
class NearbyShopStoreAPI(MethodView):
    """附近商店API"""

    @blp.arguments(NearbyStoreQueryArgSchema, location='query')
    @blp.response(ReNearbyStoreListSchema)
    def get(self, args):
        """获取附近的商店"""
        return shop_store_service.get_nearby(
            args["latitude"],
            args["longitude"],
            args.get("distance", 5.0)
        )


@blp.route('/shop-store/stats')
class ShopStoreStatsAPI(MethodView):
    """商店统计API"""
    decorators = [auth_required()]

    @blp.response(ReShopStoreStatsSchema)
    def get(self):
        """获取商店统计信息"""
        return shop_store_service.get_stats()


@blp.route('/shop-store/status')
class ShopStoreStatusAPI(MethodView):
    """商店状态API"""
    decorators = [auth_required()]

    @blp.arguments(ShopStoreStatusUpdateArgSchema)
    @blp.response(ReShopStoreSchema)
    def post(self, args):
        """更新商店状态"""
        return shop_store_service.update_status(args["id"], args["status"])


@blp.route('/shop-store/service-mode')
class ShopStoreServiceModeAPI(MethodView):
    """商店服务模式API"""
    decorators = [auth_required()]

    @blp.arguments(ServiceModeToggleArgSchema)
    @blp.response(ReShopStoreSchema)
    def post(self, args):
        """切换商店服务模式"""
        return shop_store_service.toggle_service_mode(
            args["id"],
            args["mode_type"],
            args["enabled"]
        )


@blp.route('/shop-store/business-hours')
class ShopStoreBusinessHoursAPI(MethodView):
    """商店营业时间API"""
    decorators = [auth_required()]

    @blp.arguments(BusinessHoursUpdateArgSchema)
    @blp.response(ReShopStoreSchema)
    def post(self, args):
        """更新商店营业时间"""
        return shop_store_service.update_business_hours(
            args["id"],
            args["opening_hours"]
        )


@blp.route('/shop-store/delivery-settings')
class ShopStoreDeliverySettingsAPI(MethodView):
    """商店配送设置API"""
    decorators = [auth_required()]

    @blp.arguments(DeliverySettingsUpdateArgSchema)
    @blp.response(ReShopStoreSchema)
    def post(self, args):
        """更新商店配送设置"""
        return shop_store_service.update_delivery_settings(
            args["id"],
            args["delivery_price"],
            args["min_order_amount"]
        )


@blp.route('/shop-store/contact')
class ShopStoreContactAPI(MethodView):
    """商店联系信息API"""
    decorators = [auth_required()]

    @blp.arguments(ContactInfoUpdateArgSchema)
    @blp.response(ReShopStoreSchema)
    def post(self, args):
        """更新商店联系信息"""
        return shop_store_service.update_contact_info(
            args["id"],
            args["contact_person"],
            args["contact_phone"]
        )


@blp.route('/shop-store/wifi')
class ShopStoreWifiAPI(MethodView):
    """商店WiFi设置API"""
    decorators = [auth_required()]

    @blp.arguments(WifiSettingsUpdateArgSchema)
    @blp.response(ReShopStoreSchema)
    def post(self, args):
        """更新商店WiFi设置"""
        return shop_store_service.update_wifi_settings(
            args["id"],
            args["wifi_name"],
            args["wifi_password"]
        )


@blp.route('/shop-store/by-code/<string:store_code>')
class ShopStoreByCodeAPI(MethodView):
    """通过编码获取商店API"""

    @blp.response(ReShopStoreSchema)
    def get(self, store_code: str):
        """通过商店编码获取商店信息"""
        return shop_store_service.get_by_code(store_code)
