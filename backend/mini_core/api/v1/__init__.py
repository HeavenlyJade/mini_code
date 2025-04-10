from flask_smorest import Blueprint

mini_core_v1_blp = Blueprint('小程序接口', 'mini_core', url_prefix='/api/v1/mini_core', description='小程序接口')
mini_wx_app_v1_blp = Blueprint('微信小程序接口', 'wx_mini_app', url_prefix='/api/v1/wx_mini_app', description='微信小程序接口')


