from flask.views import MethodView

from backend.business.schema.product import ProductListSchema, ProductQueryArgSchema
from backend.business.service import product_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('product', 'product', url_prefix='/products')


@blp.route('/')
class ProductAPI(MethodView):
    """产品管理API"""

    @blp.arguments(ProductQueryArgSchema, location='query')
    @blp.response(ProductListSchema)
    def get(self, args: dict):
        """产品管理 列举所有产品"""
        return product_service.list(args)
