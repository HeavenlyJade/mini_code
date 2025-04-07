from typing import Optional, List, Dict, Any
from kit.service.base import CRUDService
from backend.mini_core.domain.shop import ShopProduct,ShopProductCategory
from backend.mini_core.repository.shop.shop_sqla import ShopProductSQLARepository,ShopProductCategorySQLARepository

__all__ = ['ShopProductService','ShopProductCategoryService']


class ShopProductService(CRUDService[ShopProduct]):
    def __init__(self, repo: ShopProductSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopProductSQLARepository:
        return self._repo


    def get_list(self, args: dict) -> Dict[str, Any]:
        """根据条件获取商品"""
        product_id = args.get("id")
        if product_id:
            data = self._repo.get(product_id)
            return dict(data=data, code=200)

        # 支持按名称、编码、分类等查询
        code = args.get("code")
        name = args.get("name")
        status = args.get("status")
        is_recommended = args.get("is_recommended")
        page = args.get("page")
        size = args.get("size")
        query_params = {"need_total_count":True}
        if page:
            query_params["page"] = page
        if size:
            query_params["size"] = size
        if name:
            query_params['name'] = name
        if code:
            query_params['code'] = code
        if status:
            query_params['status'] = status
        if is_recommended is not None:
            query_params['is_recommended'] = is_recommended

        data, total = self._repo.list(**query_params)
        return dict(data=data, total=total, code=200)

    def list_by_category(self, category_id: int) -> Dict[str, Any]:
        """获取指定分类下的所有商品"""
        data = self._repo.find(category_id=category_id)
        return dict(data=data, code=200)

    def get_recommended(self) -> Dict[str, Any]:
        """获取推荐商品"""
        data = self._repo.find(is_recommended=True, status="上架")
        return dict(data=data, code=200)

    def update_stock(self, product_id: int, quantity: int) -> Dict[str, Any]:
        """更新商品库存"""
        product = self._repo.get(product_id)
        if not product:
            return dict(data=None, code=404, message="商品不存在")

        # 确保库存不小于0
        new_stock = max(0, product.stock + quantity)
        product.stock = new_stock

        # 检查是否低于库存预警值
        stock_warning = False
        if product.stock_alert and product.stock <= product.stock_alert:
            stock_warning = True

        result = self._repo.update(product_id, product)
        return dict(data=result, stock_warning=stock_warning, code=200)


    def update_pro(self, product_id: int, product:Dict) -> Dict[str, Any]:
        """更新商品信息"""
        print("product",product)
        result = super().update(product_id, product)
        return dict(data=result, code=200)

    def create_pro(self, product: Dict) -> Dict[str, Any]:
        """创建新商品"""
        result = super().create(product)
        return dict(data=result, code=200)

    def delete_pro(self, product_id: int) -> Dict[str, Any]:
        """删除商品"""
        result = super().delete(product_id)
        return dict(data=result, code=200)

    def change_status(self, product_id: int, status: str) -> Dict[str, Any]:
        """更改商品状态（上架/下架）"""
        product = self._repo.get(product_id)
        if not product:
            return dict(data=None, code=404, message="商品不存在")

        product.status = status
        result = self._repo.update(product_id, product)
        return dict(data=result, code=200)

    def toggle_recommendation(self, product_id: int) -> Dict[str, Any]:
        """切换商品推荐状态"""
        product = self._repo.get(product_id)
        if not product:
            return dict(data=None, code=404, message="商品不存在")

        product.is_recommended = not product.is_recommended
        result = self._repo.update(product_id, product)
        return dict(data=result, code=200)


class ShopProductCategoryService(CRUDService[ShopProductCategory]):
    def __init__(self, repo: ShopProductCategorySQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopProductCategorySQLARepository:
        return self._repo

    def get_list(self, args: dict) -> Dict[str, Any]:
        """根据条件获取分类"""
        category_id = args.get("id")
        if category_id:
            data = self._repo.get(category_id)
            return dict(data=data, code=200)

        # 支持按名称、编码等查询
        code = args.get("code")
        name = args.get("name")
        parent_id = args.get("parent_id")

        query_params = {}
        if code:
            query_params['code'] = code
        if name:
            query_params['name'] = name
        if parent_id:
            query_params['parent_id'] = parent_id

        data,total = self._repo.list(**query_params)
        return dict(data=data, code=200,total=total)

    def find_data(self,args: dict) -> Dict[str, Any]:
        data = self._repo.find(id=args["id"])
        return dict(data=data, code=200)

    def list_by_parent(self, parent_id: int) -> Dict[str, Any]:
        """获取指定父分类下的所有子分类"""
        data = self._repo.find(parent_id=parent_id)
        return dict(data=data, code=200)

    def get_tree(self) -> Dict[str, Any]:
        """获取分类树结构"""
        # 先获取所有分类
        all_categories = self._repo.find()

        # 构建树结构
        root_categories = []
        category_map = {}

        # 先构建一个映射
        for category in all_categories:
            category_map[category.id] = {
                "id": category.id,
                "name": category.name,
                "code": category.code,
                "children": []
            }

        # 然后构建树
        for category in all_categories:
            if not category.parent_id:
                # 根分类
                root_categories.append(category_map[category.id])
            else:
                # 子分类，添加到父分类的children中
                if category.parent_id in category_map:
                    category_map[category.parent_id]["children"].append(category_map[category.id])

        return dict(data=root_categories, code=200)

    def update(self, category_id: int, category: ShopProductCategory) -> Dict[str, Any]:
        """更新分类信息"""
        result = super().update(category_id, category)
        return dict(data=result, code=200)

    def create(self, category: ShopProductCategory) -> Dict[str, Any]:
        """创建新分类"""
        result = super().create(category)
        return dict(data=result, code=200)

    def delete(self, category_id: int) -> Dict[str, Any]:
        """删除分类"""
        result = super().delete(category_id)
        return dict(data=result, code=200)
