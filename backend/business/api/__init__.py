from backend.business.api.v1 import business_v1_blp
from backend.business.api.v1.enums import blp as e_blp
from backend.business.api.v1.product import blp as p_blp

business_v1_blp.register_blueprint(e_blp)
business_v1_blp.register_blueprint(p_blp)
