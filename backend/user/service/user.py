import datetime as dt
from typing import Optional

from flask import g
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash, generate_password_hash

from backend.extensions import casbin_enforcer, db
from backend.license_management.create_parsing_li.create_license import GetMacAddress
from backend.license_management.create_parsing_li.get_license import li_content, get_date
from backend.user import message
from backend.user.domain import User
from backend.user.message import UserMessage
from backend.user.repository.user.base import UserRepository
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService
from kit.util import casbin as casbin_util

__all__ = ['UserService']


class UserService(CRUDService[User]):
    def __init__(self, repo: UserRepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> UserRepository:
        return self._repo

    def get(self, user_id: int) -> Optional[User]:
        user = super().get(user_id)
        # from backend.user.service import department_service
        # department = department_service.get(user.department_id)
        # if department:
        #     user.department = department.name
        # self._get_user_detail(user)
        return user

    def get_user_center(self, user_id: int) -> Optional[User]:
        from backend.role.service import role_service
        casbin_enforcer.e.load_policy()
        user = self._get_user_detail(self.get(user_id))
        if user and user.role_numbers:
            role = role_service.repo.find(role_number=user.role_numbers)
            user.areas = role.areas or []
            # user.allowed_department_ids = role.get_allowed_department_ids() or []
        else:
            user.areas = []
            # user.allowed_department_ids = []
        return user

    def list(self, args: dict) -> dict:
        users, total = self.repo.list(**args)
        items = list()
        for user in users:
            # user.department = department
            item = self._get_user_detail(user)
            items.append(item)
        return dict(items=items, total=total)

    def create(self, user: User) -> User:
        current_user = get_current_user()
        user.creator = current_user.username

        if not user.password:
            user.password = message.USER_DEFAULT_PASSWORD
        user.password = generate_password_hash(user.password)
        return super().create(user)

    def update(self, entity_id: int, user: User) -> Optional[User]:
        if user.password:
            user.password = generate_password_hash(user.password)
        return super().update(entity_id, user)

    def delete(self, entity_id: int) -> None:
        user = self.get(entity_id)

        username = user.username
        if username == message.ADMIN_DEFAULT_USERNAME:
            raise ServiceBadRequest(UserMessage.ADMIN_DELETE_ERROR)
        return super().delete(entity_id)

    def login(self, args: dict):
        username = args['username']
        password = args['password']

        user = self.repo.get_by_username(username)
        if not user:
            raise ServiceBadRequest(UserMessage.USER_NOT_EXIST)

        if not self._verify_password(user.password, password):
            raise ServiceBadRequest(UserMessage.USER_PASSWORD_ERROR)
        access_token = create_access_token(user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        user.last_login_time = dt.datetime.now()
        db.session.commit()
        from backend.role.service import role_service
        role = role_service.repo.find(id=user.role_id)
        re_user =dict(username=user.username, role_id=role.id,
                      role_name=role.role_number,permission_ids=role.permission_ids,
                      id=user.id)
        return dict(access_token=access_token, refresh_token=refresh_token,user=re_user)

    def user_summary(self, department_id) -> list:
        users = self.repo.find_all(department_id=department_id)
        results = []
        for i in users:
            result = {"username": i.username, "user_id": i.id, "email": i.email}
            results.append(result)
        return dict(data=results)

    @classmethod
    def refresh_token(cls):
        user_id = get_jwt_identity()
        return dict(access_token=create_access_token(identity=user_id))

    @classmethod
    def _get_user_detail(cls, user: User) -> User:
        # permission_list = []
        # if user.role_numbers:
        #     permission_list.extend(
        #         casbin_enforcer.e.get_implicit_permissions_for_user(
        #             casbin_util.get_casbin_role_number(user.role_numbers)
        #         )
        #     )
        # user.permissions = casbin_util.get_system_permissions(permission_list)
        return user

    @classmethod
    def _verify_password(cls, pw_hash: str, password: str) -> bool:
        return check_password_hash(pw_hash, password)

    def is_li_ok(self) -> str:
        mac = GetMacAddress().mac()
        lis = self.repo.get_lis(mac)
        for i in lis:
            li_info = li_content(str(i))
            if li_info and 'end_time' in li_info.keys():
                expire_time = li_info["end_time"]
                if get_date() <= expire_time and li_info["unique_code"] == mac:
                    return str()
        return mac
