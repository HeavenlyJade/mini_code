from flask_smorest import Blueprint

user_v1_blp = Blueprint(
    '用户服务', 'users', url_prefix='/api/v1/users', description='用户服务接口'
)

department_v1_blp = Blueprint(
    '部门服务', 'departments', url_prefix='/api/v1/departments', description='部门服务接口'
)
