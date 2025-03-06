from backend.extensions import db

from .sqla import LogSQLARepository

# TODO replace this with DI
log_sqla_repo = LogSQLARepository(db.session)
