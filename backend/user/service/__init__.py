from backend.user.repository.user import user_sqla_repo
from backend.user.repository.department import department_sqla_repo

from .user import UserService
from .department import DepartmentService

user_service = UserService(user_sqla_repo)
department_service = DepartmentService(department_sqla_repo)
