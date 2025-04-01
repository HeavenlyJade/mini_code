from flask.views import MethodView

from backend.mini_core.schema.order.shop_order_setting import (
    ShopOrderSettingQueryArgSchema, ReShopOrderSettingSchema, ShopOrderSettingSchema
)
from backend.mini_core.domain.order.shop_order_setting import ShopOrderSetting
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_order_setting_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_order_setting', 'shop_order_setting', url_prefix='/')


@blp.route('/shop-order-setting')
class ShopOrderSettingAPI(MethodView):
    """订单配置API"""
    decorators = [auth_required()]

    @blp.arguments(ShopOrderSettingQueryArgSchema, location='query')
    @blp.response(ReShopOrderSettingSchema)
    def get(self, args: dict):
        """获取店铺订单配置"""
        return shop_order_setting_service.get_settings(args)

    # @blp.arguments(ShopOrderSettingSchema)
    # @blp.response(ReShopOrderSettingSchema)
    # def post(self, setting):
    #     """创建或更新店铺订单配置"""
    #     return shop_order_setting_service.create_or_update(setting)


@blp.route('/shop-order-setting/<int:setting_id>')
class ShopOrderSettingDetailAPI(MethodView):
    """订单配置详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopOrderSettingSchema)
    def get(self, setting_id: int):
        """获取指定ID的订单配置"""
        return shop_order_setting_service.get_by_id(setting_id)

    @blp.arguments(ShopOrderSettingSchema)
    @blp.response(ReShopOrderSettingSchema)
    def put(self, setting, setting_id: int):
        """更新指定ID的订单配置"""
        return shop_order_setting_service.update_setting(setting_id, setting)
    #
    # @blp.response(ReShopOrderSettingSchema)
    # def delete(self, setting_id: int):
    #     """删除指定ID的订单配置"""
    #     return shop_order_setting_service.delete_setting(setting_id)
