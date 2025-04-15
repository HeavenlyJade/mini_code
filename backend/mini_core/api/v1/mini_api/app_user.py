from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token
import uuid

from backend.mini_core.service import shop_user_service
from kit.util.blueprint import APIBlueprint

from kit.exceptions import ServiceBadRequest
from backend.mini_core.schema.shop_app.wx_login import WechatLoginSchema, ShopAppSchema
from backend.mini_core.service.shop_app import wechat_auth_service

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
            'openid':openid,
            "code":code
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
