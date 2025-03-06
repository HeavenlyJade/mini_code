from functools import wraps
from typing import Any

from flask import current_app
from flask_jwt_extended import current_user

from backend.log.service import log_service


def log(
    operation_type: int,
    operation_detail: str,
) -> Any:
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            log_service.commit(current_user.username, operation_type, operation_detail)
            return current_app.ensure_sync(fn)(*args, **kwargs)

        return decorator

    return wrapper
