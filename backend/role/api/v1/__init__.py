from flask_smorest import Blueprint

role_v1_blp = Blueprint(
    '角色服务', 'roles', url_prefix='/api/v1/roles', description='角色服务接口'
)
