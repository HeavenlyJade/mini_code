from typing import Optional, Dict, Any
from flask_jwt_extended import get_current_user
from kit.service.base import CRUDService
from backend.mini_core.domain.order.shop_order_setting import ShopOrderSetting
from backend.mini_core.repository.order.shop_order_setting_sqla  import ShopOrderSettingSQLARepository

__all__ = ['ShopOrderSettingService']


class ShopOrderSettingService(CRUDService[ShopOrderSetting]):
    def __init__(self, repo: ShopOrderSettingSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopOrderSettingSQLARepository:
        return self._repo

    def get_settings(self, args: dict) -> Dict[str, Any]:
        """根据条件获取订单配置"""
        # shop_id = args.get("shop_id")
        # if not shop_id:
        #     return dict(data=None, code=400, message="店铺ID不能为空")

        data = self._repo.get_by_shop_id()
        return dict(data=data, code=200)

    def get_by_id(self, setting_id: int) -> Dict[str, Any]:
        """获取指定ID的订单配置"""
        data = self._repo.get_by_id(setting_id)
        return dict(data=data, code=200)

    def create_or_update(self, setting: ShopOrderSetting) -> Dict[str, Any]:
        """创建或更新订单配置"""
        # 首先检查是否已存在该店铺的配置
        current_user = get_current_user()
        if hasattr(current_user, 'username'):
            setting.updater = current_user.username

        existing_setting = self._repo.get_by_shop_id(setting.shop_id)

        if existing_setting:
            # 更新
            result = self._repo.update(existing_setting.id, setting)
            return dict(data=result, code=200, message="订单配置已更新")
        else:
            # 创建
            result = self._repo.create(setting)
            return dict(data=result, code=200, message="订单配置已创建")

    def update_setting(self, setting_id: int, setting: ShopOrderSetting) -> Dict[str, Any]:
        """更新指定ID的订单配置"""
        current_user = get_current_user()
        if hasattr(current_user, 'username'):
            setting.updater = current_user.username

        result = self._repo.update(setting_id, setting)
        return dict(data=result, code=200, message="订单配置已更新")

    def delete_setting(self, setting_id: int) -> Dict[str, Any]:
        """删除指定ID的订单配置"""
        self._repo.delete(setting_id)
        return dict(code=200, message="订单配置已删除")
