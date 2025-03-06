from backend.alarm.repository.alarm import alarm_sqla_repo
from backend.alarm.repository.alarm_rule import alarm_rule_sqla_repo

from .alarm import AlarmService
from .alarm_rule import AlarmRuleService

alarm_service = AlarmService(alarm_sqla_repo)
alarm_rule_service = AlarmRuleService(alarm_rule_sqla_repo)
