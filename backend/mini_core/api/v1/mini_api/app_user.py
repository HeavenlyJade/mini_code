from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    jwt_required,
    get_jwt_identity
)

from backend.mini_core.domain.t_user import ShopUserAddress
from backend.mini_core.schema.shop_app.wx_login import WechatLoginSchema, ShopAppSchema
from backend.mini_core.schema.shop_user import (
    ShopUserAddressListSchema,
    ShopUserAddressUpdateSchema,
    SetDefaultAddressSchema,
    ShopUserAddressCreateSchema,
    ShopUserAddressSchemaRe,
    ShopUserAddressSchema,
)
from backend.mini_core.service import shop_user_address_service
from backend.mini_core.service import shop_user_service
from backend.mini_core.service.shop_app import wechat_auth_service
from kit.exceptions import ServiceBadRequest
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('wx_auth', 'wx_auth', url_prefix='/wx_auth')


@blp.route('/wechat_login')
class WechatLoginAPI(MethodView):
    """微信登录API"""

    @blp.arguments(WechatLoginSchema)
    @blp.response(ShopAppSchema)
    def post(self, args: dict):
        """使用微信临时登录凭证登录

        用户在客户端通过wx.weixinAppLogin或wx.weixinMiniProgramLogin获取code
        后端使用code换取用户信息,并创建或更新用户
        """
        code = args['code']
        nickName = args['nickName']
        # 识别平台类型 - 可从请求中获取或通过参数传递
        platform_type = args.get('platform_type', 'wx_mini_program')  # 默认为小程序

        # 通过code获取微信用户信息
        wechat_data = wechat_auth_service.code2verify_info(code)
        # 获取或创建用户
        session_key = wechat_data["session_key"]
        openid = wechat_data['openid']
        user_data = dict(
            username=nickName,
            nickName=nickName,
            avatarurl=args["avatarUrl"],
            openid=openid,
            appid=wechat_data['appid'],
            platform_type=platform_type  # 记录平台类型
        )

        if not user_data:
            raise ServiceBadRequest("无法获取微信用户信息")
        # 查询或创建用户
        if 'openid' in user_data:
            user = shop_user_service.get_or_create_wechat_user(user_data)
        else:
            raise ServiceBadRequest("无法获取微信用户标识")

        # 在token的额外声明中包含平台信息
        additional_claims = {
            "platform": platform_type,
            "appid": wechat_data['appid'],
            'openid': openid,
            "code": code
        }

        # 生成JWT令牌，并包含额外信息
        access_token = create_access_token(
            identity=user.id,
            fresh=True,
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_info': user,
            'code': 200,
            'msg': '登录成功'
        }


@blp.route('/address/set_default')
class SetShopUserAddress(MethodView):
    decorators = [jwt_required()]

    @blp.response(ShopUserAddressSchema)
    def get(self):
        """商城用户地址 获取默认地址"""
        user_id = get_jwt_identity()
        return shop_user_address_service.get_default_address(user_id)

    @blp.arguments(SetDefaultAddressSchema)
    @blp.response()
    def post(self, args: dict):
        """设置商城用户默认地址"""
        return shop_user_address_service.set_default_address(args["address_id"])


@blp.route('/address/<int:user_id>/<int:address_id>')
class FindShopUserAddress(MethodView):
    decorators = [jwt_required()]

    @blp.response(ShopUserAddressSchemaRe)
    def get(self, user_id: int, address_id: int):
        """获取商城用户的所有ID"""
        user_cache = get_current_user()
        user_id_cache = user_cache.id
        if user_id_cache != user_id:
            raise ServiceBadRequest("错误的用户")
        return shop_user_address_service.find_address(address_id, str(user_id))

    @blp.arguments(ShopUserAddressUpdateSchema)
    @blp.response(ShopUserAddressSchemaRe)
    def put(self, address: ShopUserAddress, user_id: int, address_id: int):
        """商城用户地址 编辑地址"""
        return shop_user_address_service.update(address_id, address)


@blp.route('/address/<int:user_id>')
class ShopUserAddressByIDAPI(MethodView):
    decorators = [jwt_required()]

    @blp.response(ShopUserAddressListSchema)
    def get(self, user_id: int):
        """获取商城用户的所有ID"""
        return shop_user_address_service.get_address(user_id)

    @blp.arguments(ShopUserAddressCreateSchema)
    @blp.response(ShopUserAddressSchemaRe)
    def post(self, address: ShopUserAddress, user_id: int):
        """商城用户地址 创建地址"""
        user_cache = get_current_user()
        user_id_cache = user_cache.id
        address.user_id = str(user_id_cache)
        address.updater = user_cache.username
        return shop_user_address_service.create(address)

    @blp.arguments(SetDefaultAddressSchema)
    @blp.response()
    def delete(self, args: dict, user_id: int):
        """商城用户地址 删除地址"""
        shop_user_address_service.delete_user_addr(args["address_id"], str(user_id))
        return {'code': 200, 'msg': '删除成功'}
