from flask.views import MethodView

from backend.mini_core.schema.member_level import (
    MemberLevelConfigQueryArgSchema, MemberLevelConfigCreateSchema, MemberLevelConfigUpdateSchema,
    MemberLevelConfigResponseSchema, MemberLevelConfigListResponseSchema, MemberLevelConfigSchema
)
from backend.mini_core.domain.member_level import MemberLevelConfig
from backend.business.service.auth import auth_required
from backend.mini_core.service import member_level_config_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('member_level', 'member_level', url_prefix='/member-level')


@blp.route('/')
class MemberLevelConfigAPI(MethodView):
    """会员等级配置API"""
    decorators = [auth_required()]

    @blp.arguments(MemberLevelConfigQueryArgSchema, location='query')
    @blp.response(MemberLevelConfigListResponseSchema)
    def get(self, args: dict):
        """获取会员等级配置列表"""
        return member_level_config_service.get_level_list(args)

    @blp.arguments(MemberLevelConfigCreateSchema)
    @blp.response(MemberLevelConfigResponseSchema)
    def post(self, level_data):
        """创建会员等级配置"""
        return member_level_config_service.create_level(level_data)


@blp.route('/<int:level_id>')
class MemberLevelConfigDetailAPI(MethodView):
    """会员等级配置详情API"""
    decorators = [auth_required()]

    @blp.arguments(MemberLevelConfigUpdateSchema)
    @blp.response(MemberLevelConfigResponseSchema)
    def put(self, level_data, level_id: int):
        """更新指定ID的会员等级配置"""
        return member_level_config_service.update_level(level_id, level_data)

    @blp.response(MemberLevelConfigResponseSchema)
    def delete(self, level_id: int):
        """删除指定ID的会员等级配置"""
        return member_level_config_service.delete_level(level_id)


@blp.route('/enabled')
class EnabledMemberLevelConfigAPI(MethodView):
    """启用的会员等级配置API"""

    @blp.response(MemberLevelConfigListResponseSchema)
    def get(self):
        """获取所有启用的会员等级配置"""
        return member_level_config_service.get_enabled_levels()
