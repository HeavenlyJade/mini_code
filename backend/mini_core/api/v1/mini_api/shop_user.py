from flask import jsonify
from flask.views import MethodView

from backend.business.service.auth import auth_required
from backend.extensions import jwt
from backend.mini_core.domain.t_user import ShopUser

from backend.mini_core.schema.shop_user import (
    ShopUserCreateSchema,
    ShopUserListSchema,

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

@blp.route('/')
class ShopUserAPI(MethodView):
    """商城用户管理API"""

    decorators = [auth_required()]

    @blp.arguments(ShopUserQueryArgSchema, location='query')
    @blp.response(ShopUserListSchema)
    def get(self, args: dict):
        """商城用户管理 查看用户列表"""
        return shop_user_service.list(args)


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



