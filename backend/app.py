import os
import traceback
import json
from decimal import Decimal

from flask import Flask, jsonify, request
from loguru import logger
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import FlaskParser
from flask_cors import CORS

from backend.extensions import api, casbin_enforcer, db, jwt, migrate, redis
from kit.exceptions import ServiceClientException, ServiceException
from kit.logging import configure_logger
from kit.message import GlobalMessage
from kit.util import openapi as openapi_util
from kit.util.response import APIFlask

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
def create_app() -> Flask:
    """创建Flask Application 实例"""
    app = APIFlask(__name__)
    configure_app(app)
    configure_logger(app)
    register_extensions(app)
    register_api_blueprints(app)
    register_error_handlers(app)
    register_request_handlers(app)
    app.json_encoder = CustomJSONEncoder
    CORS(app)
    return app


def configure_app(app: Flask):
    from kit.settings import config

    app.config.from_object(config.get(os.getenv('FLASK_ENV', 'development')))
    app.url_map.strict_slashes = False


def register_extensions(app: Flask):
    """注册第三方插件"""
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db=db)
    redis.init_app(app)
    casbin_enforcer.init_app(app)
    jwt.init_app(app)


def register_api_blueprints(app):
    """注册蓝图"""
    api.spec.components.security_scheme(
        'bearerAuth', {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}
    )
    api.spec.options['security'] = [{'bearerAuth': []}]
    api.ma_plugin.Converter._field2parameter = openapi_util.patched_field2parameter
    FlaskParser.DEFAULT_UNKNOWN_BY_LOCATION['json'] = None
    app.app_context().push()
    from backend.alarm.api import alarm_v1_blp
    from backend.business.api import business_v1_blp

    from backend.log.api import log_v1_blp
    from backend.role.api import role_v1_blp
    from backend.mini_core.api import mini_core_v1_blp
    from backend.user.api import user_v1_blp, department_v1_blp
    from backend.license_management.api import license_v1_blp

    blueprints = [ alarm_v1_blp, user_v1_blp, department_v1_blp,
         role_v1_blp, business_v1_blp, log_v1_blp, license_v1_blp,mini_core_v1_blp
    ]
    for blueprint in blueprints:
        api.register_blueprint(blueprint)


def register_error_handlers(app: Flask):
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(dict(message=GlobalMessage.NOT_FOUND_ERROR)), 404

    @app.errorhandler(Exception)
    def backend_exception_handler(error):
        logger.warning(traceback.format_exc())
        if isinstance(error, ServiceClientException):
            response = jsonify(dict(error))
            response.status_code = error.status_code
        elif isinstance(error, IntegrityError):
            error = ServiceException(GlobalMessage.INTEGRITY_ERROR)
            response = jsonify(dict(error))
            response.status_code = error.status_code
        elif isinstance(error, NotImplementedError):
            response = jsonify()
        else:
            logger.error(GlobalMessage.SERVER_LOG_ERROR)
            error = ServiceException(GlobalMessage.SERVER_UI_ERROR)
            response = jsonify(dict(error))
            response.status_code = error.status_code
        return response


def register_request_handlers(app: Flask):
    @app.before_request
    def log_request_body():
        logger.info('Record the request start >>>>')
        logger.info(f'Request Args is {dict(request.args)}')
        if request.is_json:
            logger.info(f'Request Body is {request.get_json(silent=True)}')
        else:
            logger.info(f'Request Body is {request.data}')
        logger.info('Record the request end <<<<')
