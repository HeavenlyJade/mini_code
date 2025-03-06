from typing import List, Optional

from flask_jwt_extended import current_user

from backend.extensions import casbin_enforcer
from backend.role import message
from backend.role.domain import Role
from backend.user.service import user_service
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService
from kit.util import casbin as casbin_util

__all__ = ['RoleService']


class RoleService(CRUDService[Role]):
    def create(self, role: Role) -> Role:
        role.creator = current_user.username
        return super().create(role)

    def update(self, role_id: int, role: Role) -> Optional[Role]:
        role.modifier = current_user.username
        return super().update(role_id, role)

    def delete(self, record_id: int):
        role = self.get(record_id)

        casbin_enforcer.e.load_policy()
        users = user_service.repo.find(role_numbers=role.role_number)
        if users:
            raise ServiceBadRequest(message.ROLE_IN_USE_ERROR)

        role_number = casbin_util.get_casbin_role_number(role.role_number)
        casbin_enforcer.e.delete_role(role_number)
        super(RoleService, self).delete(record_id)

    @classmethod
    def assign_roles_for_user(cls, username: str, role_numbers: List[str]) -> None:
        casbin_enforcer.e.delete_roles_for_user(username)
        for role_number in role_numbers:
            role_number = casbin_util.get_casbin_role_number(role_number)
            casbin_enforcer.e.add_role_for_user(username, role_number)
        casbin_enforcer.e.load_policy()

    def get_permissions(self, role_id: int) -> List[dict]:
        role = self.get(role_id)
        role_number = casbin_util.get_casbin_role_number(role.role_number)
        casbin_enforcer.e.load_policy()
        permission_list = casbin_enforcer.e.get_permissions_for_user(role_number)
        return casbin_util.get_system_permissions(permission_list)

    def assign_permissions(self, role_id: int, permissions: List[dict]) -> None:
        role = self.get(role_id)
        self.update(role_id, role)
        role_number = casbin_util.get_casbin_role_number(role.role_number)
        casbin_enforcer.e.load_policy()
        existed_permissions = {tuple(permission) for permission in casbin_enforcer.e.get_permissions_for_user(role_number)}
        permissions = {
            (role_number, permission['obj'], permission['act']) for permission in permissions
        }

        add_permissions = permissions - existed_permissions
        delete_permissions = existed_permissions - permissions

        casbin_enforcer.e.remove_policies(list(map(list, delete_permissions)))
        casbin_enforcer.e.add_policies(add_permissions)

