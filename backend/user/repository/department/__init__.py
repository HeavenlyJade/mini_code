from backend.extensions import db

from .sqla import DepartmentSQLARepository

# TODO replace this with DI
department_sqla_repo = DepartmentSQLARepository(db.session)
