from flask.views import MethodView

from backend.log.domain import Log
from backend.log.schema.log import (
    LogCreateSchema,
    LogListSchema,
    LogQueryArgSchema,
    LogSchema,
)
from backend.log.service import log_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('logs', 'logs', url_prefix='/')


@blp.route('/')
class LogAPI(MethodView):
    """日志管理API"""

    @blp.arguments(LogQueryArgSchema, location='query')
    @blp.response(LogListSchema)
    def get(self, args: dict):
        """日志管理 查看日志列表"""
        return log_service.list(args)

    @blp.arguments(LogCreateSchema)
    @blp.response(LogSchema)
    def post(self, log: Log):
        """日志管理 创建日志"""
        return log_service.commit(log.operating_user, log.operating_detail)


@blp.route('/<int:log_id>')
class LogByIDAPI(MethodView):
    @blp.response(LogSchema)
    def get(self, log_id: int):
        """日志管理 查看日志详情"""
        return log_service.get(log_id)
