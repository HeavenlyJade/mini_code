from backend.extensions import db

from .sqla import AlarmSQLARepository

# TODO replace this with DI
alarm_sqla_repo = AlarmSQLARepository(db.session)
