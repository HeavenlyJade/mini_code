import uuid
from functools import wraps
from typing import Any, Callable

from flask import g, request
from flask_jwt_extended import verify_jwt_in_request, get_current_user

from backend.user.service import department_service
from backend.role.service import role_service
from backend.role.domain.role import AccessLevel
from backend.user.message import ADMIN_DEFAULT_USERNAME


# FIXME: Simpler implementation.
# Maybe you can reference: `https://casbin.org/docs/data-permissions.`
def auth_required():
    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def decorator(*args, **kwargs) -> Any:
            verify_jwt_in_request()
            user = get_current_user()

            if request.method == 'GET':
                if user.username == ADMIN_DEFAULT_USERNAME:
                    return fn(*args, **kwargs)
                role_numbers = user.role_numbers
                role = role_service.repo.find(role_number=role_numbers)
                if role and role.areas:
                    g.areas = role.areas
                    if role.access_level == AccessLevel.TARGET_DEPT.value:
                        g.allowed_department_ids = role.allowed_department_ids
                    elif role.access_level == AccessLevel.OWN_DEPT.value:
                        g.allowed_department_ids = [user.department_id]
                    elif role.access_level == AccessLevel.OWN_SUB_DEPT.value:
                        departments = department_service.get_sub_departments(user.department_id)
                        g.allowed_department_ids = [department.id for department in departments]
                    elif role.access_level == AccessLevel.ONESELF.value:
                        g.creator = user.username
                else:
                    g.areas = [str(uuid.uuid4())]
                return fn(*args, **kwargs)
            elif request.method == 'POST':
                g.creator = user.username
                g.create_department_id = user.department_id
                return fn(*args, **kwargs)
            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper


def get_filter_args() -> dict:
    args = dict()
    if hasattr(g, 'areas'):
        args['areas'] = g.areas
    return args


def get_filter_departments_args() -> dict:
    args = dict()
    if hasattr(g, 'allowed_department_ids'):
        args['department_ids'] = g.areas
    return args
