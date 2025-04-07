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
        data = self._repo.get_by_id(category_id)
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
            return dict(data=None, code=400, message="该门店分类下有子分类，不能删除")

        result = super().delete(category_id)
        return dict(data=result, code=200)

    def batch_delete(self, category_ids: List[int]) -> Dict[str, Any]:
        """批量删除分类 - 遵循事务原子性"""
        if not category_ids:
            return dict(data=None, code=400, message="未提供要删除的分类ID")

        # 预检查所有分类
        error_messages = []
        for category_id in category_ids:
            children = self._repo.find(parent_id=category_id)
            if children:
                error_messages.append(f"分类ID {category_id} 下有子分类，无法删除")

        # 如果有任何错误，整个操作失败
        if error_messages:
            return dict(
                data=None,
                code=400,
                message="批量删除失败: " + "; ".join(error_messages)
            )
        # 所有检查都通过，执行批量删除
        try:
            self._repo.batch_delete(ids=category_ids)
            # 只有所有删除都成功时才提交事务
            return dict(
                data={"deleted_ids": category_ids},
                code=200,
                message=f"成功删除了 {len(category_ids)} 个分类"
            )

        except Exception as e:
            # 如有异常，事务会自动回滚（根据你的数据库框架实现）
            return dict(
                data=None,
                code=500,
                message=f"批量删除过程中发生错误: {str(e)}"
            )
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
