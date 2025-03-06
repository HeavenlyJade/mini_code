from typing import Optional

from backend.alarm.domain import AlarmRule
from kit.service.base import CRUDService

__all__ = ['AlarmRuleService']


class AlarmRuleService(CRUDService[AlarmRule]):
    def find(self, **kwargs) -> Optional[AlarmRule]:
        return self.repo.find(**kwargs)

    def create_or_update_rule(self, alarm_rule: AlarmRule):
        rule = self.repo.find()
        if rule:
            return self.update(rule.id, alarm_rule)
        return self.create(alarm_rule)
