from typing import Optional, List, Dict, Any
from kit.service.base import CRUDService
from backend.mini_core.domain.store import ShopStore
from backend.mini_core.repository.store.store_sqla import ShopStoreSQLARepository

__all__ = ['ShopStoreService']


class ShopStoreService(CRUDService[ShopStore]):
    def __init__(self, repo: ShopStoreSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopStoreSQLARepository:
        return self._repo

    def get_store(self, args: dict) -> Dict[str, Any]:
        """根据条件获取商店信息"""
        store_id = args.get("id")
        if store_id:
            data = self._repo.get(store_id)
            return dict(data=data, code=200)

        # 支持按名称、编码、分类等查询
        name = args.get("name")
        store_code = args.get("store_code")
        type = args.get("type")
        store_category = args.get("store_category")
        province = args.get("province")
        status = args.get("status")

        query_params = {}
        if name:
            query_params['name'] = name
        if store_code:
            query_params['store_code'] = store_code
        if type:
            query_params['type'] = type
        if store_category:
            query_params['store_category'] = store_category
        if province:
            query_params['province'] = province
        if status:
            query_params['status'] = status

        data, total = self._repo.list(**query_params)
        return dict(data=data, code=200, total=total)

    def get_by_id(self, store_id: int) -> Dict[str, Any]:
        """获取指定ID的商店"""
        data = self._repo.get(store_id)
        return dict(data=data, code=200)

    def get_by_category(self, category_id: int) -> Dict[str, Any]:
        """获取指定分类下的所有商店"""
        data = self._repo.get_stores_by_category(category_id)
        return dict(data=data, code=200)

    def search(self, keyword: str) -> Dict[str, Any]:
        """搜索商店"""
        data = self._repo.search_stores(keyword)
        return dict(data=data, code=200)

    def get_nearby(self, latitude: float, longitude: float, distance: float = 5.0) -> Dict[str, Any]:
        """获取附近的商店"""
        data = self._repo.get_nearby_stores(latitude, longitude, distance)
        return dict(data=data, code=200)

    def get_stats(self) -> Dict[str, Any]:
        """获取商店统计信息"""
        data = self._repo.get_store_stats()
        return dict(data=data, code=200)

    def update_store(self, store_id: int, store: Dict) -> Dict[str, Any]:
        """更新商店信息"""
        result = super().update(store_id, store)
        return dict(data=result, code=200)

    def create_store(self, store: Dict) -> Dict[str, Any]:
        """创建新商店"""
        result = super().create(store)
        return dict(data=result, code=200)

    def delete_store(self, store_id: int) -> Dict[str, Any]:
        """删除商店"""
        result = super().delete(store_id)
        return dict(data=result, code=200)

    def update_status(self, store_id: int, status: str) -> Dict[str, Any]:
        """更新商店状态（正常/停用）"""
        store = self._repo.get(store_id)
        if not store:
            return dict(data=None, code=404, message="商店不存在")

        if status not in ["正常", "停用"]:
            return dict(data=None, code=400, message="状态值无效")

        store.status = status
        result = self._repo.update(store)
        return dict(data=result, code=200)

    def update_sort_order(self, store_id: int, sort_order: int) -> Dict[str, Any]:
        """更新商店排序"""
        store = self._repo.get(store_id)
        if not store:
            return dict(data=None, code=404, message="商店不存在")

        store.sort_order = sort_order
        result = self._repo.update(store)
        return dict(data=result, code=200)

    def get_by_code(self, store_code: str) -> Dict[str, Any]:
        """通过商店编码获取商店信息"""
        data = self._repo.find(store_code=store_code)
        if not data:
            return dict(data=None, code=404, message="商店不存在")
        return dict(data=data[0], code=200)

    def toggle_service_mode(self, store_id: int, mode_type: str, enabled: bool) -> Dict[str, Any]:
        """
        切换服务模式状态

        Args:
            store_id: 商店ID
            mode_type: 模式类型 (takeout_enabled, self_pickup_enabled, dine_in_enabled)
            enabled: 是否启用
        """
        store = self._repo.get(store_id)
        if not store:
            return dict(data=None, code=404, message="商店不存在")

        if mode_type not in ["takeout_enabled", "self_pickup_enabled", "dine_in_enabled"]:
            return dict(data=None, code=400, message="模式类型无效")

        setattr(store, mode_type, enabled)
        result = self._repo.update(store)
        return dict(data=result, code=200)

    def update_business_hours(self, store_id: int, opening_hours: str) -> Dict[str, Any]:
        """更新营业时间"""
        store = self._repo.get(store_id)
        if not store:
            return dict(data=None, code=404, message="商店不存在")

        store.opening_hours = opening_hours
        result = self._repo.update(store)
        return dict(data=result, code=200)

    def update_delivery_settings(self, store_id: int, delivery_price: float, min_order_amount: float) -> Dict[str, Any]:
        """更新配送设置"""
        store = self._repo.get(store_id)
        if not store:
            return dict(data=None, code=404, message="商店不存在")

        store.delivery_price = delivery_price
        store.min_order_amount = min_order_amount
        result = self._repo.update(store)
        return dict(data=result, code=200)

    def update_contact_info(self, store_id: int, contact_person: str, contact_phone: str) -> Dict[str, Any]:
        """更新联系信息"""
        store = self._repo.get(store_id)
        if not store:
            return dict(data=None, code=404, message="商店不存在")

        store.contact_person = contact_person
        store.contact_phone = contact_phone
        result = self._repo.update(store)
        return dict(data=result, code=200)

    def update_wifi_settings(self, store_id: int, wifi_name: str, wifi_password: str) -> Dict[str, Any]:
        """更新WiFi设置"""
        store = self._repo.get(store_id)
        if not store:
            return dict(data=None, code=404, message="商店不存在")

        store.wifi_name = wifi_name
        store.wifi_password = wifi_password
        result = self._repo.update(store)
        return dict(data=result, code=200)
