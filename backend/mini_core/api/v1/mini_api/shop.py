from flask.views import MethodView
from typing import List

from backend.mini_core.schema.shop import (
    ProductCategoryQueryArgSchema, ReProductCategorySchema, ReProductCategoryListSchema,
    ShopProductQueryArgSchema, ReShopProductSchema, ReShopProductListSchema,
    ShopProductStockUpdateArgSchema, ShopProductStatusUpdateArgSchema,
    ReShopProductStockUpdateSchema, ReProductCategoryTreeSchema,ProductCategorySchema,ShopProductSchema,
    ProductCategoryBatchDeleteSchema
)
from kit.schema.base import  FieldQuerySchema
from backend.mini_core.domain.shop import ShopProduct, ShopProductCategory
from backend.business.service.auth import auth_required
from backend.mini_core.service import (
    shop_product_service, shop_product_category_service
)
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop', 'shop', url_prefix='/')




@blp.route('/product-category')
class ProductCategoryAPI(MethodView):
    """商品分类API"""

    @blp.arguments(ProductCategoryQueryArgSchema, location='query')
    @blp.response(ReProductCategoryListSchema)
    def get(self, args: dict):
        """查询商品分类列表"""
        return shop_product_category_service.get_list(args)


@blp.route('/product-category/<int:category_id>')
class ProductCategoryDetailAPI(MethodView):
    """商品分类详情API"""

    @blp.response(ReProductCategorySchema)
    def get(self, category_id: int):
        """获取指定ID的商品分类"""
        return shop_product_category_service.find_data({"id": category_id})

    @blp.arguments(ProductCategorySchema)
    @blp.response(ReProductCategorySchema)
    def put(self, category, category_id: int):
        """更新指定ID的商品分类"""
        return shop_product_category_service.update(category_id, category)

    @blp.response(ReProductCategorySchema)
    def delete(self, category_id: int):
        """删除指定ID的商品分类"""
        return shop_product_category_service.delete(category_id)

@blp.route('/shop-product')
class ShopProductAPI(MethodView):
    """商品API"""

    @blp.arguments(ShopProductQueryArgSchema, location='query')
    @blp.response(ReShopProductListSchema)
    def get(self, args: dict):
        """查询商品列表"""
        return shop_product_service.get_list(args)



@blp.route('/shop-product/<int:product_id>')
class ShopProductDetailAPI(MethodView):
    """商品详情API"""

    @blp.response(ReShopProductSchema)
    def get(self, product_id: int):
        """获取指定ID的商品"""
        data = shop_product_service.get({"id": product_id})
        return dict(code=200,data=data)





@blp.route('/shop-product/category/<int:category_id>')
class ShopProductByCategoryAPI(MethodView):
    """按分类查询商品API"""

    @blp.response(ReShopProductListSchema)
    def get(self, category_id: int):
        """获取指定分类下的所有商品"""
        return shop_product_service.list_by_category(category_id)


@blp.route('/shop-product/recommended')
class ShopProductRecommendedAPI(MethodView):
    """推荐商品API"""

    @blp.response(ReShopProductListSchema)
    def get(self):
        """获取所有推荐商品"""
        return shop_product_service.get_recommended()





