from backend.log.domain import Log
from kit.service.base import CRUDService

__all__ = ['LogService']


class LogService(CRUDService[Log]):
    @classmethod
    def commit(cls, operating_user: str, operating_type: int, operating_detail: str):
        from task.log import commit_log
        commit_log.delay(operating_user, operating_type, operating_detail)
