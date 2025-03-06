from flask.views import MethodView

from backend.alarm.domain import AlarmRule
from backend.alarm.schema.alarm_rule import AlarmRuleSchema, AlarmRuleUpdateSchema
from backend.alarm.service import alarm_rule_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('alarm_rules', 'alarm_rules', url_prefix='/rules')


@blp.route('/')
class AlarmRuleAPI(MethodView):
    """异常规则管理API"""

    @blp.response(AlarmRuleSchema)
    def get(self):
        """异常规则管理 查看异常规则"""
        return alarm_rule_service.find()

    @blp.arguments(AlarmRuleUpdateSchema)
    @blp.response(AlarmRuleSchema)
    def put(self, alarm_rule: AlarmRule):
        """异常规则管理 修改异常规则"""
        return alarm_rule_service.create_or_update_rule(alarm_rule)
