from backend.log.domain import Log
from kit.service.base import CRUDService

__all__ = ['LogService']  # 注意这里应该是双下划线


class LogService(CRUDService[Log]):
    @classmethod
    def commit(cls, operating_user: str, operating_type: int, operating_detail: str):
        # 在方法内部导入而不是在模块顶部导入
        from task.log import commit_log
        commit_log.delay(operating_user, operating_type, operating_detail)
