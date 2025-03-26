from typing import Optional, List, Dict, Any
from kit.service.base import CRUDService
from backend.mini_core.domain.store import ShopStoreCategory
from backend.mini_core.repository.store.store_car_sqla import ShopStoreCategorySQLARepository

__all__ = ['ShopStoreCategoryService']


class ShopStoreCategoryService(CRUDService[ShopStoreCategory]):
    def __init__(self, repo: ShopStoreCategorySQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopStoreCategorySQLARepository:
        return self._repo

    def get_list(self, args: dict) -> Dict[str, Any]:
        """根据条件获取分类列表"""
        category_id = args.get("id")
        if category_id:
            data = self._repo.get(category_id)
            return dict(data=data, code=200)

        # 支持按名称、编码等查询
        code = args.get("code")
        name = args.get("name")
        parent_id = args.get("parent_id")
        status = args.get("status")

        query_params = {}
        if code:
            query_params['code'] = code
        if name:
            query_params['name'] = name
        if parent_id is not None:
            query_params['parent_id'] = parent_id
        if status:
            query_params['status'] = status

        data, total = self._repo.list(**query_params)
        return dict(data=data, code=200, total=total)

    def get_by_id(self, category_id: int) -> Dict[str, Any]:
        """获取指定ID的分类"""
        data = self._repo.get(category_id)
        return dict(data=data, code=200)

    def list_by_parent(self, parent_id: int) -> Dict[str, Any]:
        """获取指定父分类下的所有子分类"""
        data = self._repo.find(parent_id=parent_id)
        return dict(data=data, code=200)

    def get_tree(self) -> Dict[str, Any]:
        """获取分类树结构"""
        tree_data = self._repo.get_category_tree()
        return dict(data=tree_data, code=200)

    def update(self, category_id: int, category: ShopStoreCategory) -> Dict[str, Any]:
        """更新分类信息"""
        result = super().update(category_id, category)
        return dict(data=result, code=200)

    def create(self, category: ShopStoreCategory) -> Dict[str, Any]:
        """创建新分类"""
        result = super().create(category)
        return dict(data=result, code=200)

    def delete(self, category_id: int) -> Dict[str, Any]:
        """删除分类"""
        # 检查是否有子分类
        children = self._repo.find(parent_id=category_id)
        if children:
            return dict(data=None, code=400, message="该分类下有子分类，不能删除")

        result = super().delete(category_id)
        return dict(data=result, code=200)

    def toggle_recommend(self, category_id: int) -> Dict[str, Any]:
        """切换分类的推荐状态"""
        category = self._repo.get(category_id)
        if not category:
            return dict(data=None, code=404, message="分类不存在")

        category.is_recommend = not category.is_recommend
        result = self._repo.update(category)
        return dict(data=result, code=200)

    def update_status(self, category_id: int, status: str) -> Dict[str, Any]:
        """更新分类状态"""
        category = self._repo.get(category_id)
        if not category:
            return dict(data=None, code=404, message="分类不存在")

        if status not in ["正常", "停用"]:
            return dict(data=None, code=400, message="状态值无效")

        category.status = status
        result = self._repo.update(category)
        return dict(data=result, code=200)
