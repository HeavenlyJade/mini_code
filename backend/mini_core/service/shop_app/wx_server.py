import requests
from typing import Dict, Any, Optional
from flask import current_app


class WechatAuthService:
    """微信认证服务"""

    @staticmethod
    def code2verify_info(code: str) -> Dict[str, Any]:
        """
        将微信临时登录凭证换取用户信息

        参数:
            code: 来自wx.weixinAppLogin/wx.weixinMiniProgramLogin的临时登录凭证

        返回:
            包含用户信息的字典

        异常:
            Exception: 如果API请求失败
        """
        # 从应用配置中获取多平台应用配置
        appid = current_app.config.get('WECHAT_MULTIPLATFORM_APPID')
        appsecret = current_app.config.get('WECHAT_MULTIPLATFORM_SECRET')

        if not appid or not appsecret:
            raise ValueError("未配置微信多平台应用凭证")

        # 准备请求参数
        params = {
            'appid': appid,
            'secret': appsecret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        # 向微信API发送请求
        api_url = 'https://api.weixin.qq.com/sns/jscode2session'
        response = requests.get(api_url, params=params)
        result = response.json()
        # 检查错误
        session_key = result.get('session_key')
        openid = result.get('openid') #用户唯一标识
        if not session_key or not openid:
            errmsg = result.get('errmsg')
            return dict(code=400,msg=f"用户错误:{errmsg}")
        return dict(session_key=session_key, openid=openid,appid=appid,)

