from flask.views import MethodView

from backend.mini_core.schema.member_level import (
    MemberLevelConfigQueryArgSchema,  MemberLevelConfigListResponseSchema,
)
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


