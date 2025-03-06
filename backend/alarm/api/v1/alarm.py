from flask.views import MethodView

from backend.alarm.domain import Alarm
from backend.alarm.schema.alarm import (
    AlarmCreateSchema,
    AlarmListSchema,
    AlarmQueryArgSchema,
    AlarmSchema,
)
from backend.alarm.service import alarm_service
from backend.business.service.auth import auth_required, get_filter_args
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('alarms', 'alarms', url_prefix='/')


@blp.route('/')
class AlarmAPI(MethodView):
    """报警管理API"""

    decorators = [auth_required()]

    @blp.arguments(AlarmQueryArgSchema, location='query')
    @blp.response(AlarmListSchema)
    def get(self, args: dict):
        """报警管理 查看报警列表"""
        args.update(get_filter_args())
        return alarm_service.list(args)

    @blp.arguments(AlarmCreateSchema)
    @blp.response(AlarmSchema)
    def post(self, alarm: Alarm):
        """报警管理 创建报警信息"""
        return alarm_service.create(alarm)
