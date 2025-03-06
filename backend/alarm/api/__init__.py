from backend.alarm.api.v1 import alarm_v1_blp
from backend.alarm.api.v1.alarm import blp as a_blp
from backend.alarm.api.v1.alarm_rule import blp as r_blp

alarm_v1_blp.register_blueprint(a_blp)
alarm_v1_blp.register_blueprint(r_blp)
