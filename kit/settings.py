import json
from collections import defaultdict
from enum import Enum, unique
from pathlib import Path

from environs import Env

from kit import filename

env = Env()
env.read_env(override=True)


class Config:
    @unique
    class ServerEnv(Enum):
        DEV = 'development'
        TEST = 'testing'
        PROD = 'production'

    # Project
    VERSION = env.str('VERSION')

    # Flask
    FLASK_ENV = env.str('FLASK_ENV', default=ServerEnv.DEV.value)
    SECRET_KEY = env.str('SECRET_KEY')

    # Logging
    LOG_PATH = env.path('LOG_PATH')
    LOG_LEVEL = env.str('LOG_LEVEL')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = env.str('DEV_DATABASE_URL')
    SQLALCHEMY_POOL_SIZE = env.int('SQLALCHEMY_POOL_SIZE')
    SQLALCHEMY_POOL_RECYCLE = env.int('SQLALCHEMY_POOL_RECYCLE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    sqlalchemy_binds_str = env("SQLALCHEMY_BINDS", "{}")
    SQLALCHEMY_BINDS = json.loads(sqlalchemy_binds_str)


    # Multiple databases support.
    DATABASE_TYPE = SQLALCHEMY_DATABASE_URI.split(':')[0]

    # API Openapi Doc
    API_TITLE = '起源小程序'
    API_VERSION = VERSION
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_JSON_PATH = 'api-spec.json'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_REDOC_URL = (
        'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
    )
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/'
    OPENAPI_RAPIDOC_PATH = '/rapidoc'
    OPENAPI_RAPIDOC_URL = (
        'https://cdn.jsdelivr.net/npm/rapidoc@9.3.2/dist/rapidoc-min.min.js'
    )

    # Redis
    REDIS_URL = env.str('REDIS_URL')
    REDIS_SENTINEL_NODES = env.list('REDIS_SENTINEL_NODES', list())
    REDIS_CLUSTER_NODES = env.list('REDIS_CLUSTER_NODES', list())
    REDIS_PASSWORD = env.str('REDIS_PASSWORD', None)
    AREAS = env.list('AREAS', list())

    # Casbin
    CASBIN_MODEL_PATH = str(
        Path(filename.CONF_FOLDER, 'casbin/rbac_with_resource_roles_model.conf')
    )
    ENABLE_WATCHER = env.bool('ENABLE_WATCHER', False)

    # JWT
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = env.int('JWT_ACCESS_TOKEN_EXPIRES')
    JWT_DECODE_LEEWAY = env.int('JWT_DECODE_LEEWAY')
    JWT_ERROR_MESSAGE_KEY = 'message'

    # Storage
    BUCKET_NAME = env.str('BUCKET_NAME')
    LOCAL_STORAGE_PATH = env.path('LOCAL_STORAGE_PATH')


    # Equipment Service
    EQUIPMENT_REPO_TYPE = env.str('EQUIPMENT_REPO_TYPE', 'sqla')

    # Kafka
    BOOTSTRAP_SERVERS = env.str('BOOTSTRAP_SERVERS')
    # Web Service
    WEB_SERVICE_URL_PREFIX = env.str('WEB_SERVICE_URL_PREFIX')

    # RabbitMQ
    RABBITMQ_SERVERS = env.str("RABBITMQ_SERVERS")
    ELK_IP = env.str("ELK_IP")
    ELK_LISTENER_PORT = env.int('ELK_LISTENER_PORT')
    ELK_TAGS = env.str('ELK_TAGS')
    ELK_VERSION = env.str("ELK_VERSION")

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_BACKTRACE = True
    SQLALCHEMY_DATABASE_URI = env.str('DEV_DATABASE_URL')
    OPENAPI_URL_PREFIX = 'docs'


class TestingConfig(Config):
    TESTING = True
    LOG_BACKTRACE = True
    SQLALCHEMY_DATABASE_URI = env.str('TEST_DATABASE_URL')
    OPENAPI_URL_PREFIX = 'docs'


class ProductionConfig(Config):
    LOG_BACKTRACE = False
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')


config = defaultdict(
    lambda: DevelopmentConfig,
    dict(
        development=DevelopmentConfig,
        testing=TestingConfig,
        production=ProductionConfig,
    ),
)
