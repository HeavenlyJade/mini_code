from flask_smorest import Blueprint

business_v1_blp = Blueprint(
    '业务服务', 'business', url_prefix='/api/v1/business', description='业务服务接口'
)
