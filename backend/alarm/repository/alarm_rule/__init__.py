from backend.extensions import db

from .sqla import AlarmRuleSQLARepository

# TODO replace this with DI
alarm_rule_sqla_repo = AlarmRuleSQLARepository(db.session)
