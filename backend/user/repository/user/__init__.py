from backend.extensions import db

from .sqla import UserSQLARepository

# TODO replace this with DI
user_sqla_repo = UserSQLARepository(db.session)
