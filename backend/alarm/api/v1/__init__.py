from flask_smorest import Blueprint

alarm_v1_blp = Blueprint(
    '报警服务', 'equipments', url_prefix='/api/v1/alarm', description='报警服务接口'
)
