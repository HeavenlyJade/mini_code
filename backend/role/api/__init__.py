from backend.role.api.v1 import role_v1_blp
from backend.role.api.v1.role import blp as e_blp

role_v1_blp.register_blueprint(e_blp)
