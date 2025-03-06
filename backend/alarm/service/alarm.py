from typing import Any, Optional

from backend.alarm.domain import Alarm
from kit.service.base import CRUDService

__all__ = ['AlarmService']


class AlarmService(CRUDService[Alarm]):
    def create_alarm(self, message: str, task_id: Optional[str] = None) -> Alarm:
        return self.repo.create(
            Alarm(message=message, task_id=task_id)
        )
