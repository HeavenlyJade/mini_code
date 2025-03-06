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
