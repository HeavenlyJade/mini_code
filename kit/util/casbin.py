from typing import List


def get_casbin_role_number(role_number: str) -> str:
    return f'role::{role_number}'


def get_system_role_number(casbin_role_number: str) -> str:
    return casbin_role_number.split('::')[-1]


def get_system_permissions(permission_list: List[list]) -> List[dict]:
    permissions = list()
    for permission in permission_list:
        _, obj, act = permission
        permissions.append(dict(obj=obj, act=act))
    return permissions
