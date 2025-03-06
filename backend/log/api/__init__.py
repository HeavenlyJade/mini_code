from backend.log.api.v1 import log_v1_blp
from backend.log.api.v1.log import blp as e_blp

log_v1_blp.register_blueprint(e_blp)
