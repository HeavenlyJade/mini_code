from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.business.service.auth import auth_required
from backend.extensions import jwt
from backend.log import log_service
from backend.log.domain.log import LogOperatingType
from backend.user.domain import User
from backend.user.message import AuthMessage
from backend.user.schema.user import (
    LoginSchema,
    RefreshTokenSchema,
    TokenSchema,
    UserCenterUpdateSchema,
    UserCreateSchema,
    UserListSchema,
    UserPatchSchema,
    UserQueryArgSchema,
    UserSchema,
    UserUpdateSchema,
)
from backend.user.service import user_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('users', 'users', url_prefix='/')

@blp.route('/login')
class LoginAPI(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(TokenSchema)
    def post(self, args: dict):
        """用户管理 用户登录"""
        # is_ok = user_service.is_li_ok()
        # if is_ok:
        #     return {'msg': 'License has expired ', 'access_token': is_ok, 'code': 561}

        tokens = user_service.login(args)
        # log_service.commit(
        #     args['username'], LogOperatingType.LOGIN.value, f'{args["username"]}登录系统'
        # )
        return tokens


@blp.route('/refresh')
class TokenRefreshAPI(MethodView):
    @jwt_required(refresh=True)
    @blp.response(RefreshTokenSchema)
    def post(self):
        """用户管理 刷新Token"""
        return user_service.refresh_token()


@blp.route('/')
class UserAPI(MethodView):
    """用户管理API"""

    decorators = [auth_required()]

    @blp.arguments(UserQueryArgSchema, location='query')
    @blp.response(UserListSchema)
    def get(self, args: dict):
        """用户管理 查看用户列表"""
        return user_service.list(args)

    @blp.arguments(UserCreateSchema)
    @blp.response(UserSchema)
    def post(self, user: User):
        """用户管理 创建用户"""
        return user_service.create(user)


@blp.route('/<int:user_id>')
class UserByIDAPI(MethodView):
    decorators = [auth_required()]

    @blp.response(UserSchema)
    def get(self, user_id: int):
        """用户管理 查看用户详情"""
        return user_service.get(user_id)

    @blp.arguments(UserUpdateSchema)
    @blp.response(UserSchema)
    def put(self, user: User, user_id: int):
        """用户管理 编辑用户"""
        return user_service.update(user_id, user)

    @blp.arguments(UserPatchSchema)
    @blp.response(UserSchema)
    def patch(self, user: User, user_id: int):
        """用户管理 更新用户"""
        return user_service.update(user_id, user)

    @blp.response(RespSchema)
    def delete(self, user_id: int):
        """用户管理 删除用户信息"""
        return user_service.delete(user_id)


@blp.route('/center')
class UserCenterAPI(MethodView):
    decorators = [jwt_required()]

    @blp.response(UserSchema)
    def get(self):
        """用户管理 查看用户中心信息"""
        user_id = get_jwt_identity()
        return user_service.get_user_center(user_id)

    @blp.arguments(UserCenterUpdateSchema)
    @blp.response(UserSchema)
    def put(self, user: User):
        """用户管理 修改用户中心信息"""
        user_id = get_jwt_identity()
        return user_service.update(user_id, user)


@blp.route('/<int:department_id>/user_summary')
class DepartmentUserAPI(MethodView):
    @blp.response()
    def get(self, department_id: int):
        """部门管理 查看部门详情"""
        return user_service.user_summary(department_id)
