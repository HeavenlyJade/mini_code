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
            # 验证 JWT 并获取数据
            jwt_header, jwt_data = verify_jwt_in_request()

            # 从 JWT 载荷中提取平台相关信息
            openid = jwt_data.get('sub')  # 标准 JWT 中身份通常存储在 sub 字段
            # 获取当前用户对象
            user = get_current_user()

            # 将平台相关信息存储到 Flask 全局变量中
            for key in ['platform', 'appid']:
                if key in jwt_data:
                    setattr(g, key, jwt_data[key])

            # 微信用户不需要进一步的权限检查
            if openid:
                return fn(*args, **kwargs)

            # 非微信用户的权限处理
            if request.method == 'GET':
                # 管理员直接通过
                if user.username == ADMIN_DEFAULT_USERNAME:
                    return fn(*args, **kwargs)

                # 处理基于角色的权限
                role_numbers = user.role_numbers
                role = role_service.repo.find(role_number=role_numbers)

                if role and role.areas:
                    g.areas = role.areas

                    # 根据访问级别设置部门权限
                    if role.access_level == AccessLevel.TARGET_DEPT.value:
                        g.allowed_department_ids = role.allowed_department_ids
                    elif role.access_level == AccessLevel.OWN_DEPT.value:
                        g.allowed_department_ids = [user.department_id]
                    # elif role.access_level == AccessLevel.OWN_SUB_DEPT.value:
                    #     departments = department_service.get_sub_departments(user.department_id)
                    #     g.allowed_department_ids = [department.id for department in departments]
                    elif role.access_level == AccessLevel.ONESELF.value:
                        g.creator = user.username
                else:
                    # 没有指定区域的情况下，使用随机 UUID 作为限制
                    g.areas = [str(uuid.uuid4())]

            elif request.method == 'POST':
                # POST 请求保存创建者信息
                g.creator = user.username
                g.create_department_id = user.department_id

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
