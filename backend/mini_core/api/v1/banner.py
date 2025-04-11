# backend/business/api/v1/banner.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from backend.mini_core.domain.banner import Banner
from backend.mini_core.schema.banner import (
    BannerCreateSchema,
    BannerListSchema,
    BannerQueryArgSchema,
    BannerSchema,
    BannerStatusSchema,
    BannerUpdateSchema,
)
from backend.mini_core.service import banner_service
from backend.business.service.auth import auth_required
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('banners', 'banners', url_prefix='/banners')


@blp.route('/')
class BannerAPI(MethodView):
    """Banner管理API"""

    decorators = [auth_required()]

    @blp.arguments(BannerQueryArgSchema, location='query')
    @blp.response(BannerListSchema)
    def get(self, args: dict):
        """Banner管理 查看Banner列表"""
        return banner_service.list(args)

    @blp.arguments(BannerCreateSchema)
    @blp.response(BannerSchema)
    def post(self, banner: Banner):
        """Banner管理 创建Banner"""
        return banner_service.create(banner)


@blp.route('/<int:banner_id>')
class BannerByIDAPI(MethodView):
    decorators = [auth_required()]

    @blp.response(BannerSchema)
    def get(self, banner_id: int):
        """Banner管理 查看Banner详情"""
        return banner_service.get(banner_id)

    @blp.arguments(BannerUpdateSchema)
    @blp.response(BannerSchema)
    def put(self, banner: Banner, banner_id: int):
        """Banner管理 编辑Banner"""
        return banner_service.update(banner_id, banner)

    @blp.response(RespSchema)
    def delete(self, banner_id: int):
        """Banner管理 删除Banner"""
        return banner_service.delete(banner_id)


@blp.route('/<int:banner_id>/status')
class BannerStatusAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(BannerStatusSchema)
    @blp.response(BannerSchema)
    def patch(self, args: dict, banner_id: int):
        """Banner管理 更新Banner状态"""
        return banner_service.update_status(banner_id, args['status'])


@blp.route('/by-type/<string:code_type>')
class BannerByTypeAPI(MethodView):
    @blp.response(BannerListSchema)
    def get(self, code_type: str):
        """获取指定类型的Banner列表"""
        banners = banner_service.get_by_code_type(code_type)
        return {'items': banners, 'total': len(banners)}


@blp.route('/by-type/<string:code_type>/code/<string:business_code>')
class BannerByTypeAndCodeAPI(MethodView):
    @blp.response(BannerListSchema)
    def get(self, code_type: str, business_code: str):
        """获取指定类型和业务编号的Banner列表"""
        banners = banner_service.get_by_code_type(code_type, business_code)
        return {'items': banners, 'total': len(banners)}
