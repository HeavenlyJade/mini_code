import os
import json
import time
import uuid
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import requests
from typing import Dict, Any, Optional
from flask import current_app
import random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256 as CryptoSHA256


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


class WechatPayService:
    """微信支付服务"""

    @staticmethod
    def create_jsapi_order(args: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建微信JSAPI支付订单

        参数:
            args: 包含订单信息的字典

        返回:
            包含预支付交易会话标识的字典
        """
        from flask_jwt_extended import  get_current_user

        # 从配置中获取支付相关参数
        app_id = current_app.config.get('WECHAT_MULTIPLATFORM_APPID')
        mch_id = current_app.config.get('WECHAT_MULTIPLATFORM_MCHID')
        notify_url = current_app.config.get('WECHAT_PAY_NOTIFY_URL')

        order_id = args.get("order_id")
        user = get_current_user()
        openid = user.openid

        if not all([app_id, mch_id, notify_url, order_id, openid]):
            return {"status": "fail", "error": "参数不完整", "code": 400}

        # 从订单服务获取订单数据
        from backend.mini_core.service import shop_order_service
        order_result = shop_order_service.get_order_by_id(order_id)
        if order_result.get("code") != 200 or not order_result.get("data"):
            return {"error": "订单不存在", "code": 400}
        order_data = order_result.get("data")
        # 构建请求数据
        data = {
            "appid": app_id,
            "mchid": mch_id,
            "description": f"订单{order_data.order_no}购买",
            "out_trade_no": order_data.order_no,  # 使用订单编号作为商户订单号
            "notify_url": notify_url,
            "amount": {
                "total": int(order_data.actual_amount * 100),  # 订单总金额，单位为分
                "currency": "CNY"
            },
            "payer": {
                "openid": openid  # 用户OpenID必填
            }
        }

        # 添加可选参数
        if args.get("time_expire"):
            data["time_expire"] = args.get("time_expire")
        args_data = WechatPayService._generate_authorization(data, mch_id)
        Authorization= args_data.get("authorization")
        # 构建HTTP请求头
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": Authorization
        }

        # 发送请求到微信支付API
        api_url = "https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi"
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        result = response.json()
        print(result)
        if response.status_code == 200 and "prepay_id" in result:
            prepay_id = result.get("prepay_id")

            # 使用新的JSAPI调起支付签名方法
            jsapi_params = WechatPayService._generate_author_jsapi({
                "appid": app_id,
                "prepay_id": prepay_id
            })

            return dict(data=jsapi_params, code=200, order_no=order_data.order_no)
        else:
            return dict(error=result.get("message", "支付下单失败"), code=400)

    @staticmethod
    def _generate_authorization(data: Dict[str, Any], mch_id: str) -> dict:
        """
        生成微信支付API v3签名
        按照微信支付v3 API规范生成签名

        参数:
            data: 请求数据
            mch_id: 商户号

        返回:
            授权头字符串
        """
        # 使用当前工作目录获取商户API私钥
        root_path = os.getcwd()
        private_key_path = os.path.join(root_path, "wxcert", "apiclient_key.pem")
        merchant_serial_number = current_app.config.get('WECHAT_MULTIPLATFORM_SERIAL')

        # 生成随机字符串
        # 改用新的随机字符串生成方法
        nonce_str = str(uuid.uuid4()).replace("-","")


        # 获取当前时间戳
        timestamp = str(int(time.time()))
        # 请求方法
        method = 'POST'
        # 请求路径
        url_path = '/v3/pay/transactions/jsapi'
        # 请求体
        body = json.dumps(data)

        # 构造签名串 - 按照微信支付文档格式
        sign_str = f"{method}\n{url_path}\n{timestamp}\n{nonce_str}\n{body}\n"

        # 读取私钥文件内容 - 确保私钥文件格式正确
        with open(private_key_path, 'r') as f:
            private_key = f.read()
            # 确保私钥内容格式正确，需要包含BEGIN和END行，以及中间的私钥内容
            if "-----BEGIN PRIVATE KEY-----" not in private_key or "-----END PRIVATE KEY-----" not in private_key:
                raise ValueError("私钥文件格式不正确")

        # 使用pycryptodome库进行签名
        pkey = RSA.importKey(private_key)
        h = CryptoSHA256.new(sign_str.encode('utf-8'))
        signature_bytes = PKCS1_v1_5.new(pkey).sign(h)
        signature = base64.b64encode(signature_bytes).decode('utf-8')

        # 构造Authorization头，按照文档要求使用正确的参数名
        authorization = (f'WECHATPAY2-SHA256-RSA2048 '
                         f'mchid="{mch_id}",'
                         f'nonce_str="{nonce_str}",'
                         f'signature="{signature}",'
                         f'timestamp="{timestamp}",'
                         f'serial_no="{merchant_serial_number}"')

        return dict(authorization=authorization,time_stamp=timestamp,nonce_str=nonce_str,pay_sign=signature)

    @staticmethod
    def _generate_author_jsapi(data: Dict[str, Any]) -> dict:
        """
        生成JSAPI调起支付的签名

        参数:
            data: 包含appid和prepay_id的字典

        返回:
            包含签名和其他支付参数的字典
        """
        # 使用当前工作目录获取商户私钥
        root_path = os.getcwd()
        private_key_path = os.path.join(root_path, "wxcert", "apiclient_key.pem")
        # 从参数中获取appid和prepay_id
        app_id = data.get("appid")
        prepay_id = data.get("prepay_id")

        if not all([app_id, prepay_id]):
            raise ValueError("缺少必要的参数：appid或prepay_id")

        # 1. 获取时间戳
        timestamp = str(int(time.time()))

        # 2. 生成随机字符串
        chars = "123456789zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
        nonce_str = ''.join(random.sample(chars, 30))

        # 3. 构造签名串 - 注意每行都以\n结束，包括最后一行
        package = f"prepay_id={prepay_id}"
        sign_str = f"{app_id}\n{timestamp}\n{nonce_str}\n{package}\n"

        # 4. 读取私钥
        try:
            with open(private_key_path, 'r') as f:
                private_key = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到私钥文件：{private_key_path}")

        # 5. 使用pycryptodome库签名
        from Crypto.PublicKey import RSA
        from Crypto.Signature import PKCS1_v1_5
        from Crypto.Hash import SHA256

        pkey = RSA.importKey(private_key)
        h = SHA256.new(sign_str.encode('utf-8'))
        signature_bytes = PKCS1_v1_5.new(pkey).sign(h)
        pay_sign = base64.b64encode(signature_bytes).decode('utf-8')

        # 6. 返回调起支付所需的所有参数
        return {
            "app_id": app_id,
            "time_stamp": timestamp,
            "nonce_str": nonce_str,
            "package": package,
            "sign_type": "RSA",
            "pay_sign": pay_sign
        }

    @staticmethod
    def verify_notify_signature(timestamp: str, nonce: str, body: bytes,
                               signature: str, serial: str) -> bool:
        """
        验证微信支付回调通知的签名

        参数:
            timestamp: 时间戳
            nonce: 随机字符串
            body: 请求体
            signature: 签名
            serial: 证书序列号

        返回:
            签名验证结果
        """
        try:
            # 获取微信平台证书
            # 实际项目中需要实现证书管理，定期更新证书
            platform_cert = WechatPayService._get_platform_certificate(serial)

            # 构造验签名串
            message = f"{timestamp}\n{nonce}\n{body.decode('utf-8')}\n"

            # 使用平台证书验证签名
            # 实际项目中需要实现完整的验签逻辑
            # 这里仅为示例
            verify_result = True  # 替换为实际验签结果

            return verify_result
        except Exception as e:
            current_app.logger.error(f"验证签名异常: {str(e)}")
            return False

    @staticmethod
    def decrypt_notify_data(resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        解密微信支付通知数据

        参数:
            resource: 包含加密数据的资源对象

        返回:
            解密后的数据
        """
        try:
            # 获取解密所需信息
            algorithm = resource.get('algorithm')
            ciphertext = resource.get('ciphertext')
            associated_data = resource.get('associated_data', '')
            nonce = resource.get('nonce')

            # 获取API V3密钥
            api_v3_key = current_app.config.get('WECHAT_PAY_API_V3_KEY')

            if algorithm != 'AEAD_AES_256_GCM':
                raise ValueError(f"不支持的加密算法: {algorithm}")

            # Base64解码密文
            ciphertext_bytes = base64.b64decode(ciphertext)

            # 使用AEAD_AES_256_GCM算法解密
            aes_gcm = AESGCM(api_v3_key.encode('utf-8'))
            decrypted_bytes = aes_gcm.decrypt(
                nonce.encode('utf-8'),
                ciphertext_bytes,
                associated_data.encode('utf-8') if associated_data else None
            )

            # 将解密后的数据转换为字典
            decrypted_data = json.loads(decrypted_bytes.decode('utf-8'))

            return decrypted_data
        except Exception as e:
            current_app.logger.error(f"解密通知数据异常: {str(e)}")
            return {}

    @staticmethod
    def process_payment_result(payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理支付结果

        参数:
            payment_data: 支付结果数据

        返回:
            处理结果
        """
        try:
            # 获取支付结果关键信息
            out_trade_no = payment_data.get('out_trade_no')
            transaction_id = payment_data.get('transaction_id')
            trade_state = payment_data.get('trade_state')

            # 记录日志
            current_app.logger.info(f"收到支付结果通知: 商户订单号={out_trade_no}, 交易状态={trade_state}")

            # 验证订单是否存在
            # TODO: 实现订单查询逻辑

            # 检查支付状态
            if trade_state == 'SUCCESS':
                # 更新订单状态为支付成功
                # TODO: 实现订单状态更新逻辑

                # 执行其他业务逻辑，如发货、增加积分等
                # TODO: 实现相关业务逻辑

                return {"success": True}
            else:
                # 处理其他支付状态
                current_app.logger.warning(f"支付未成功，状态为: {trade_state}")
                return {"success": False, "error": f"支付状态: {trade_state}"}

        except Exception as e:
            current_app.logger.error(f"处理支付结果异常: {str(e)}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def _get_platform_certificate(serial: str) -> Any:
        """
        获取微信支付平台证书
        实际项目中需要实现证书管理

        参数:
            serial: 证书序列号

        返回:
            平台证书
        """
        # TODO: 实现证书获取和管理逻辑
        return None




