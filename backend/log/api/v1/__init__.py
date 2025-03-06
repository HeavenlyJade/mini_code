from flask_smorest import Blueprint

log_v1_blp = Blueprint('日志服务', 'logs', url_prefix='/api/v1/logs', description='日志服务接口')
