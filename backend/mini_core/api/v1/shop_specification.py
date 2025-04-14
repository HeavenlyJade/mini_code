from flask.views import MethodView

from backend.mini_core.schema.shop_specification import (
    ShopSpecificationQueryArgSchema, ReShopSpecificationSchema, ReShopSpecificationListSchema,
    ShopSpecificationAttributeQueryArgSchema, ReShopSpecificationAttributeSchema, ReShopSpecificationAttributeListSchema,
    DeleteIdsSchema, ReSpecificationWithAttributesSchema,
    ShopSpecificationSchema, ShopSpecificationAttributeSchema
)
from backend.mini_core.domain.specification import ShopSpecification, ShopSpecificationAttribute
from backend.business.service.auth import auth_required
from backend.mini_core.service import shop_specification_service, shop_specification_attribute_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('specification', 'specification', url_prefix='/')


@blp.route('/shop-specification')
class ShopSpecificationAPI(MethodView):
    """商品规格API"""
    decorators = [auth_required()]

    @blp.arguments(ShopSpecificationQueryArgSchema, location='query')
    @blp.response(ReShopSpecificationListSchema)
    def get(self, args: dict):
        """查询商品规格列表"""
        return shop_specification_service.get_list(args)

    @blp.arguments(ShopSpecificationSchema)
    @blp.response(ReShopSpecificationSchema)
    def post(self, specification):
        """创建商品规格"""
        return shop_specification_service.create_specification(specification)


@blp.route('/shop-specification/<int:specification_id>')
class ShopSpecificationDetailAPI(MethodView):
    """商品规格详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopSpecificationSchema)
    def get(self, specification_id: int):
        """获取指定ID的商品规格"""
        return shop_specification_service.get_by_id(specification_id)

    @blp.arguments(ShopSpecificationSchema)
    @blp.response(ReShopSpecificationSchema)
    def put(self, specification, specification_id: int):
        """更新指定ID的商品规格"""
        return shop_specification_service.update_specification(specification_id, specification)

    @blp.response(ReShopSpecificationSchema)
    def delete(self, specification_id: int):
        """删除指定ID的商品规格"""
        return shop_specification_service.delete_specification(specification_id)


@blp.route('/shop-specification/batch-delete')
class ShopSpecificationBatchDeleteAPI(MethodView):
    """批量删除商品规格API"""
    decorators = [auth_required()]

    @blp.arguments(DeleteIdsSchema)
    def post(self, args):
        """批量删除商品规格"""
        return shop_specification_service.batch_delete(args["ids"])


@blp.route('/shop-specification/<int:specification_id>/with-attributes')
class ShopSpecificationWithAttributesAPI(MethodView):
    """商品规格及其属性API"""
    decorators = [auth_required()]

    @blp.response(ReSpecificationWithAttributesSchema)
    def get(self, specification_id: int):
        """获取商品规格及其属性"""
        return shop_specification_service.get_with_attributes(specification_id)


@blp.route('/shop-specification-attribute')
class ShopSpecificationAttributeAPI(MethodView):
    """商品规格属性API"""
    decorators = [auth_required()]

    @blp.arguments(ShopSpecificationAttributeQueryArgSchema, location='query')
    @blp.response(ReShopSpecificationAttributeListSchema)
    def get(self, args: dict):
        """查询商品规格属性列表"""
        return shop_specification_attribute_service.get_list(args)

    @blp.arguments(ShopSpecificationAttributeSchema)
    @blp.response(ReShopSpecificationAttributeSchema)
    def post(self, attribute):
        """创建商品规格属性"""
        return shop_specification_attribute_service.create_attribute(attribute)


@blp.route('/shop-specification-attribute/<int:attribute_id>')
class ShopSpecificationAttributeDetailAPI(MethodView):
    """商品规格属性详情API"""
    decorators = [auth_required()]

    @blp.response(ReShopSpecificationAttributeSchema)
    def get(self, attribute_id: int):
        """获取指定ID的商品规格属性"""
        return shop_specification_attribute_service.get_by_id(attribute_id)

    @blp.arguments(ShopSpecificationAttributeSchema)
    @blp.response(ReShopSpecificationAttributeSchema)
    def put(self, attribute, attribute_id: int):
        """更新指定ID的商品规格属性"""
        return shop_specification_attribute_service.update_attribute(attribute_id, attribute)

    @blp.response(ReShopSpecificationAttributeSchema)
    def delete(self, attribute_id: int):
        """删除指定ID的商品规格属性"""
        return shop_specification_attribute_service.delete_attribute(attribute_id)


@blp.route('/shop-specification-attribute/batch-delete')
class ShopSpecificationAttributeBatchDeleteAPI(MethodView):
    """批量删除商品规格属性API"""
    decorators = [auth_required()]

    @blp.arguments(DeleteIdsSchema)
    def post(self, args):
        """批量删除商品规格属性"""
        return shop_specification_attribute_service.batch_delete(args["ids"])


@blp.route('/shop-specification/<int:specification_id>/attributes')
class ShopSpecificationAttributesBySpecificationAPI(MethodView):
    """指定规格的属性API"""
    decorators = [auth_required()]

    @blp.response(ReShopSpecificationAttributeListSchema)
    def get(self, specification_id: int):
        """获取指定规格ID的所有属性"""
        return shop_specification_attribute_service.get_by_specification(specification_id)
