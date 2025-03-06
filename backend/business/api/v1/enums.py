from flask.views import MethodView

from backend.business.service import enum_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('enums', 'enum', url_prefix='/enums')


@blp.route('/')
class EnumAPI(MethodView):
    """枚举管理API"""

    def get(self):
        """枚举管理 列举所有枚举"""
        return enum_service.list()
