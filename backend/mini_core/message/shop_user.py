class ShopUserMessage:
    USER_NOT_EXIST = '用户不存在'
    USER_PASSWORD_ERROR = '用户名不存在或密码错误'
    USER_EXISTED = '用户已存在'
    PHONE_EXISTED = '手机号已被使用'
    OPENID_EXISTED = 'OpenID已被使用'
    USER_DISABLED = '用户已被禁用'


class ShopAuthMessage:
    TOKEN_EXPIRES = '登录失效，请重新登录'
