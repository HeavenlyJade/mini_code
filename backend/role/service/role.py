from typing import List, Optional

from flask_jwt_extended import current_user
from backend.role.repository.role import role_sqla_repo
from backend.extensions import casbin_enforcer
from backend.role import message
from backend.role.domain import Role
from backend.user.service import user_service
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService
from kit.util import casbin as casbin_util

__all__ = ['RoleService']


class RoleService(CRUDService[Role]):

    def __init__(self, repo: role_sqla_repo, ):
        super().__init__(repo)
        self._repo = repo
    def create(self, role: Role) -> Role:
        role.creator = current_user.username
        return super().create(role)

    def update(self, role_id: int, role: Role) -> Optional[Role]:
        role.modifier = current_user.username
        print("role",role)
        return self._repo.update_data(role_id, role)

    def delete(self, record_id: int):
        role = self.get(record_id)
        users = user_service.repo.find(role_numbers=role.role_number)
        if users:
            raise ServiceBadRequest(message.ROLE_IN_USE_ERROR)
        super(RoleService, self).delete(record_id)




