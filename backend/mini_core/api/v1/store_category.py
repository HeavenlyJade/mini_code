from flask.views import MethodView

from backend.mini_core.schema.store.store_category import (
    ShopStoreCategoryQueryArgSchema, ReShopStoreCategorySchema, ReShopStoreCategoryListSchema,
    ShopStoreCategoryStatusUpdateArgSchema, ReShopStoreCategoryTreeSchema
)
from backend.mini_core.domain.store import ShopStoreCategory
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_store_category_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_store_category', 'shop_store_category', url_prefix='/')


@blp.route('/shop-store-category')
class ShopStoreCategoryAPI(MethodView):
    """商店分类API"""
    decorators = [auth_required()]

    @blp.arguments(ShopStoreCategoryQueryArgSchema, location='query')
    @blp.response(ReShopStoreCategoryListSchema)
    def get(self, args: dict):
        """查询商店分类列表"""
        return shop_store_category_service.get_list(args)

    @blp.arguments(ShopStoreCategory)
    @blp.response(ReShopStoreCategorySchema)
    def post(self, category):
        """创建或更新商店分类"""
        if category.get("id"):
            return shop_store_category_service.update(category["id"], category)
        else:
            return shop_store_category_service.create(category)


@blp.route('/shop-store-category/<int:category_id>')
class ShopStoreCategoryDetailAPI(MethodView):
    """商店分类详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopStoreCategorySchema)
    def get(self, category_id: int):
        """获取指定ID的商店分类"""
        return shop_store_category_service.get_by_id(category_id)

    @blp.arguments(ShopStoreCategory)
    @blp.response(ReShopStoreCategorySchema)
    def put(self, category, category_id: int):
        """更新指定ID的商店分类"""
        return shop_store_category_service.update(category_id, category)

    @blp.response(ReShopStoreCategorySchema)
    def delete(self, category_id: int):
        """删除指定ID的商店分类"""
        return shop_store_category_service.delete(category_id)


@blp.route('/shop-store-category/tree')
class ShopStoreCategoryTreeAPI(MethodView):
    """商店分类树API"""

    @blp.response(ReShopStoreCategoryTreeSchema)
    def get(self):
        """获取商店分类树结构"""
        return shop_store_category_service.get_tree()


@blp.route('/shop-store-category/children/<int:parent_id>')
class ShopStoreCategoryChildrenAPI(MethodView):
    """商店子分类API"""

    @blp.response(ReShopStoreCategoryListSchema)
    def get(self, parent_id: int):
        """获取指定父分类下的所有子分类"""
        return shop_store_category_service.list_by_parent(parent_id)


@blp.route('/shop-store-category/status')
class ShopStoreCategoryStatusAPI(MethodView):
    """商店分类状态API"""
    decorators = [auth_required()]

    @blp.arguments(ShopStoreCategoryStatusUpdateArgSchema)
    @blp.response(ReShopStoreCategorySchema)
    def post(self, args):
        """更新商店分类状态"""
        return shop_store_category_service.update_status(args["id"], args["status"])


@blp.route('/shop-store-category/toggle-recommend/<int:category_id>')
class ShopStoreCategoryToggleRecommendAPI(MethodView):
    """切换商店分类推荐状态API"""
    decorators = [auth_required()]

    @blp.response(ReShopStoreCategorySchema)
    def post(self, category_id: int):
        """切换商店分类的推荐状态"""
        return shop_store_category_service.toggle_recommend(category_id)


@blp.route('/shop-store-category/by-code/<string:code>')
class ShopStoreCategoryByCodeAPI(MethodView):
    """通过编码获取商店分类API"""

    @blp.response(ReShopStoreCategorySchema)
    def get(self, code: str):
        """通过编码获取商店分类信息"""
        args = {"code": code}
        return shop_store_category_service.get_list(args)
