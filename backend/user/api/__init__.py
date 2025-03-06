from backend.user.api.v1 import user_v1_blp
from backend.user.api.v1 import department_v1_blp
from backend.user.api.v1.user import blp as e_blp
from backend.user.api.v1.department import blp as d_blp

user_v1_blp.register_blueprint(e_blp)
department_v1_blp.register_blueprint(d_blp)

