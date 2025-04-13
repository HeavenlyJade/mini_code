ADMIN_DEFAULT_USERNAME = 'admin'  # 系统默认管理员名称
USER_DEFAULT_PASSWORD = 'admin123'  # 系统默认用户密码


class UserMessage:
    USER_NOT_EXIST = '用户不存在'
    USER_PASSWORD_ERROR = '用户名不存在或密码错误'
    ROLE_NOT_EXIST = '角色不存在'
    ADMIN_DELETE_ERROR = '系统管理员不允许删除'
    USER_EXISTED = '用户已存在'


class AuthMessage:
    TOKEN_EXPIRES = '登录失效，请重新登录'


"""
权限管理相关的消息常量
"""

# 权限相关错误消息
PERMISSION_EXISTS = '权限编号已存在'
PERMISSION_NOT_FOUND = '权限不存在'
PERMISSION_HAS_CHILDREN = '该权限下有子权限，不能删除'
PERMISSION_IN_USE = '该权限已被角色使用，不能删除'

# 成功消息
PERMISSION_CREATE_SUCCESS = '权限创建成功'
PERMISSION_UPDATE_SUCCESS = '权限更新成功'
PERMISSION_DELETE_SUCCESS = '权限删除成功'
