# __init__.py
from backend.extensions import db

from .sqla import PermissionSQLARepository

# TODO replace this with DI
permission_sqla_repo = PermissionSQLARepository(db.session)
