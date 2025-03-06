from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from sqlalchemy.orm import registry

from kit.hook import RedisHook, SocketIOApp, SqlAHook
from kit.hook.casbin import CasbinEnforcer

api = Api()
db = SqlAHook()
migrate = Migrate()
metadata = db.metadata
mapper_registry = registry(metadata=metadata)
redis = RedisHook()
sio = SocketIOApp()
casbin_enforcer = CasbinEnforcer()
jwt = JWTManager()
