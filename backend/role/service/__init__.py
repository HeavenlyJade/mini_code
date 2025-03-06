from backend.role.repository.role import role_sqla_repo

from .role import RoleService

role_service = RoleService(role_sqla_repo)
