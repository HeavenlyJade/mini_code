from backend.extensions import db

from .sqla import RoleSQLARepository

# TODO replace this with DI
role_sqla_repo = RoleSQLARepository(db.session)
