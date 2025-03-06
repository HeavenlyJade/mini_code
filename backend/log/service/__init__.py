from backend.log.repository.log import log_sqla_repo

from .log import LogService

log_service = LogService(log_sqla_repo)
