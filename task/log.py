import datetime as dt
from typing import Optional
from backend.log.domain import Log
# 移除这行: from backend.log.service import log_service
from task import celery


@celery.task
def commit_log(
    operating_user: str,
    operating_type: int,
    operating_detail: str,
    operating_time: Optional[dt.datetime] = None,
):
    operating_time = operating_time or dt.datetime.now()
    log = Log(operating_user, operating_type, operating_detail)
    log.operating_time = operating_time

    # 在这里导入以避免循环引用
    from backend.log.service import log_service
    log_service.create(log)
