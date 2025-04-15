from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.business.service.auth import auth_required
from backend.extensions import jwt
from backend.mini_core.domain.t_user import ShopUser
from backend.mini_core.message.shop_user import ShopAuthMessage
from backend.mini_core.schema.shop_user import (
    ShopLoginSchema,
    ShopWechatLoginSchema,
    RefreshTokenSchema,
    ShopTokenSchema,
    ShopUserCreateSchema,
    ShopUserListSchema,
    ShopUserPatchSchema,
    ShopUserQueryArgSchema,
    ShopUserSchema,
    ShopUserStatusSchema,
    ShopUserUpdateSchema,
)
from backend.mini_core.service import shop_user_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint
from backend.user.service import user_service
from backend.user.message import AuthMessage
from backend.user.domain import User

blp = APIBlueprint('shop_users', 'shop_users', url_prefix='/shop_users')

@jwt.user_lookup_loader
def user_loader_callback(jwt_header: dict, jwt_data: dict) -> User:
    openid = jwt_data.get("openid")
    platform = jwt_data.get("platform")
    if openid :
        return shop_user_service.find(openid=openid)
    else:
        return user_service.get(jwt_data['sub'])


@jwt.expired_token_loader
def expire_token_callback(jwt_header: dict, jwt_payload: dict):
    return jsonify(message=AuthMessage.TOKEN_EXPIRES,code=401), 401


# @blp.route('/login')
# class ShopLoginAPI(MethodView):
#     @blp.arguments(ShopLoginSchema)
#     @blp.response(ShopTokenSchema)
#     def post(self, args: dict):
#         """商城用户 用户登录"""
#         return shop_user_service.login(args)


# @blp.route('/wechat/login')
# class ShopWechatLoginAPI(MethodView):
#     @blp.arguments(ShopWechatLoginSchema)
#     @blp.response(ShopTokenSchema)
#     def post(self, args: dict):
#         """商城用户 微信用户登录"""
#         return shop_user_service.wechat_login(args)


# @blp.route('/refresh')
# class ShopTokenRefreshAPI(MethodView):
#     @jwt_required(refresh=True)
#     @blp.response(RefreshTokenSchema)
#     def post(self):
#         """商城用户 刷新Token"""
#         return shop_user_service.refresh_token()
#

@blp.route('/')
class ShopUserAPI(MethodView):
    """商城用户管理API"""

    decorators = [auth_required()]

    @blp.arguments(ShopUserQueryArgSchema, location='query')
    @blp.response(ShopUserListSchema)
    def get(self, args: dict):
        """商城用户管理 查看用户列表"""
        return shop_user_service.list(args)

    @blp.arguments(ShopUserCreateSchema)
    @blp.response(ShopUserSchema)
    def post(self, user: ShopUser):
        """商城用户管理 创建用户"""
        return shop_user_service.create(user)


@blp.route('/<int:user_id>')
class ShopUserByIDAPI(MethodView):
    decorators = [auth_required()]

    @blp.response(ShopUserSchema)
    def get(self, user_id: int):
        """商城用户管理 查看用户详情"""
        return shop_user_service.get(user_id)

    @blp.arguments(ShopUserUpdateSchema)
    @blp.response(ShopUserSchema)
    def put(self, user: ShopUser, user_id: int):
        """商城用户管理 编辑用户"""
        return shop_user_service.update(user_id, user)

    @blp.arguments(ShopUserPatchSchema)
    @blp.response(ShopUserSchema)
    def patch(self, user: ShopUser, user_id: int):
        """商城用户管理 更新用户部分信息"""
        return shop_user_service.update(user_id, user)

    @blp.response(RespSchema)
    def delete(self, user_id: int):
        """商城用户管理 删除用户信息"""
        shop_user_service.delete(user_id)
        return {'code': 200, 'msg': '删除成功'}


@blp.route('/<int:user_id>/status')
class ShopUserStatusAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(ShopUserStatusSchema)
    @blp.response(ShopUserSchema)
    def patch(self, args: dict, user_id: int):
        """商城用户管理 更新用户状态"""
        return shop_user_service.update_status(user_id, args['status'])


@blp.route('/profile')
class ShopUserProfileAPI(MethodView):
    decorators = [jwt_required()]

    @blp.response(ShopUserSchema)
    def get(self):
        """商城用户管理 查看当前登录用户信息"""
        user_id = get_jwt_identity()
        return shop_user_service.get(user_id)

    @blp.arguments(ShopUserUpdateSchema)
    @blp.response(ShopUserSchema)
    def put(self, user: ShopUser):
        """商城用户管理 修改当前用户信息"""
        user_id = get_jwt_identity()
        return shop_user_service.update(user_id, user)
