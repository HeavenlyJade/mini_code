# -*- coding: utf-8 -*-
import base64
import json
import logging
import os
import time
import uuid

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flask import current_app
from flask_jwt_extended import get_current_user
from loguru import logger

from kit.wechatpayv3 import WeChatPay, WeChatPayType


# 配置获取方式改为从Flask current_app中获取
def get_config():
    """从Flask应用配置中获取微信支付相关配置"""
    config = {
        # 微信支付商户号
        'MCHID': current_app.config.get('WECHAT_MULTIPLATFORM_MCHID'),
        # 商户API私钥路径
        'PRIVATE_KEY_PATH': os.path.join(os.getcwd(), "wxcert", "apiclient_key.pem"),
        "PUBLIC_KEY_PATH": os.path.join(os.getcwd(), "wxcert", "pub_key.pem"),
        # 商户证书序列号
        'CERT_SERIAL_NO': current_app.config.get('WECHAT_MULTIPLATFORM_SERIAL'),
        # API v3密钥
        'APIV3_KEY': current_app.config.get('WECHAT_MULTIPLATFORM_PAY'),
        # 应用ID
        'APPID': current_app.config.get('WECHAT_MULTIPLATFORM_APPID'),
        # 回调地址
        'NOTIFY_URL': current_app.config.get('WECHAT_PAY_NOTIFY_URL'),
        # 证书缓存目录
        'CERT_DIR': os.path.join(os.getcwd(), "wxcert"),
        "MULTIPLATFORM_PAY": current_app.config.get('WECHAT_MULTIPLATFORM_PAY'),

    }

    # 读取私钥
    try:
        with open(config['PRIVATE_KEY_PATH'], 'r') as f:
            config['PRIVATE_KEY'] = f.read()
    except FileNotFoundError:
        current_app.logger.error(f"找不到私钥文件：{config['PRIVATE_KEY_PATH']}")
        config['PRIVATE_KEY'] = None
    with open(config['PUBLIC_KEY_PATH'], 'r') as f:
        config['PUBLIC_KEY'] = f.read()

    return config


def init_wechat_pay():
    """初始化微信支付客户端"""
    config = get_config()

    # 日志配置
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), 'wechatpay.log'),
        level=logging.DEBUG,
        filemode='a',
        format='%(asctime)s - %(process)s - %(levelname)s: %(message)s'
    )
    logger = logging.getLogger("wechatpay")
    # 初始化微信支付客户端
    print("config",config)
    wxpay = WeChatPay(
        wechatpay_type=WeChatPayType.MINIPROG,  # 默认为JSAPI，可在调用时覆盖
        mchid=config['MCHID'],
        private_key=config['PRIVATE_KEY'],
        cert_serial_no=config['CERT_SERIAL_NO'],
        apiv3_key=config['APIV3_KEY'],
        appid=config['APPID'],
        notify_url=config['NOTIFY_URL'],
        cert_dir=config['CERT_DIR'],
        public_key=config["PUBLIC_KEY"],
        public_key_id = config["MULTIPLATFORM_PAY"],
        logger=logger,
        partner_mode=False,  # 直连商户模式
        timeout=(10, 30)  # 连接超时和读取超时
    )

    return wxpay


class WechatPayService:
    """微信支付服务"""

    @staticmethod
    def create_jsapi_order(args):
        """
        创建微信JSAPI支付订单

        参数:
            args: 包含订单信息的字典

        返回:
            包含预支付交易会话标识的字典
        """
        # 获取当前用户和订单信息
        order_id = args.get("order_id")
        user = get_current_user()
        openid = user.openid

        # 获取配置
        config = get_config()
        app_id = config['APPID']
        mchid = config['MCHID']
        notify_url = config['NOTIFY_URL']

        if not all([app_id, mchid, notify_url, order_id, openid]):
            return {"status": "fail", "error": "参数不完整", "code": 400}

        # 从订单服务获取订单数据
        from backend.mini_core.service import shop_order_service
        order_result = shop_order_service.get_order_by_id(order_id)
        if order_result.get("code") != 200 or not order_result.get("data"):
            return {"error": "订单不存在", "code": 400}

        order_data = order_result.get("data")

        # 初始化微信支付客户端
        wxpay = init_wechat_pay()
        if not wxpay:
            return {"error": "微信支付初始化失败", "code": 500}

        # 构建支付参数
        description = f"订单{order_data.order_no}购买"
        out_trade_no = order_data.order_no
        amount = {'total': int(float(order_data.actual_amount) * 100)}  # 先转为 float 再转为 int

        payer = {'openid': openid}

        # 可选参数
        optional_params = {}
        if args.get("time_expire"):
            optional_params['time_expire'] = args.get("time_expire")

        # 调用微信支付API
        code, message = wxpay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount=amount,
            pay_type=WeChatPayType.JSAPI,
            payer=payer,
            **optional_params
        )

        result = json.loads(message)
        logger.warning(f"微信字符的api结构，{result}")
        if code in range(200, 300) and "prepay_id" in result:
            prepay_id = result.get("prepay_id")

            # 生成JSAPI调起支付的参数
            timestamp = str(int(time.time()))
            nonce_str = str(uuid.uuid4()).replace('-', '')
            package = f'prepay_id={prepay_id}'

            # 使用签名方法
            sign = wxpay.sign([app_id, timestamp, nonce_str, package])

            # 构建返回参数
            jsapi_params = {
                "app_id": app_id,
                "time_stamp": timestamp,
                "nonce_str": nonce_str,
                "package": package,
                "sign_type": "RSA",
                "pay_sign": sign
            }

            return {"data": jsapi_params, "code": 200, "order_no": order_data.order_no}
        else:
            return {"error": result.get("message", "支付下单失败"), "code": 400}

    @staticmethod
    def decrypt_notify_data(resource):
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
    def process_payment_result(payment_data):
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
    def query_order(args):
        """
        查询微信支付订单

        参数:
            args: 包含查询条件的字典，可以包含 transaction_id 或 out_trade_no

        返回:
            包含订单信息的字典
        """
        # 获取查询参数
        transaction_id = args.get("transaction_id")
        out_trade_no = args.get("out_trade_no")

        if not (transaction_id or out_trade_no):
            return {"error": "缺少查询参数，需要提供交易ID或商户订单号", "code": 400}

        # 获取配置
        config = get_config()
        mchid = config['MCHID']

        # 初始化微信支付客户端
        wxpay = init_wechat_pay()
        if not wxpay:
            return {"error": "微信支付初始化失败", "code": 500}

        try:
            # 调用微信支付查询API
            code, message = wxpay.query(
                transaction_id=transaction_id,
                out_trade_no=out_trade_no,
                mchid=mchid
            )

            result = json.loads(message)
            if code in range(200, 300):
                # 查询成功，返回订单信息
                return {
                    "data": result,
                    "code": 200
                }
            else:
                # 查询失败，返回错误信息
                return {
                    "error": result.get("message", "订单查询失败"),
                    "code": code
                }

        except Exception as e:
            current_app.logger.error(f"查询订单异常: {str(e)}")
            return {"error": f"查询订单异常: {str(e)}", "code": 500}

    @staticmethod
    def refund_order(args):
        """
        申请退款

        参数:
            args: 包含退款信息的字典

        返回:
            包含退款结果的字典
        """
        # 获取退款参数
        out_refund_no = args.get("out_refund_no")  # 商户退款单号
        transaction_id = args.get("transaction_id")  # 微信支付订单号
        out_trade_no = args.get("out_trade_no")  # 商户订单号
        refund_amount = args.get("refund_amount")  # 退款金额
        total_amount = args.get("total_amount")  # 订单总金额
        refund_reason = args.get("reason")  # 退款原因

        # 验证必要参数
        if not out_refund_no:
            return {"error": "缺少商户退款单号", "code": 400}

        if not (transaction_id or out_trade_no):
            return {"error": "缺少订单标识，需要提供交易ID或商户订单号", "code": 400}

        if not (refund_amount and total_amount):
            return {"error": "缺少退款金额或订单总金额", "code": 400}

        # 初始化微信支付客户端
        wxpay = init_wechat_pay()
        if not wxpay:
            return {"error": "微信支付初始化失败", "code": 500}

        try:
            # 构建退款金额信息
            # 注意: 将金额转换为整数，单位为分
            amount = {
                "refund": int(float(refund_amount) * 100),
                "total": int(float(total_amount) * 100),
                "currency": "CNY"
            }

            # 调用微信支付退款API
            code, message = wxpay.refund(
                out_refund_no=out_refund_no,
                amount=amount,
                transaction_id=transaction_id,
                out_trade_no=out_trade_no,
                reason=refund_reason
            )

            result = json.loads(message)
            if code in range(200, 300):
                # 退款申请成功，返回退款信息
                return {
                    "data": result,
                    "code": 200,
                    "message": "退款申请成功"
                }
            else:
                # 退款申请失败，返回错误信息
                return {
                    "error": result.get("message", "退款申请失败"),
                    "code": code
                }

        except Exception as e:
            current_app.logger.error(f"申请退款异常: {str(e)}")
            return {"error": f"申请退款异常: {str(e)}", "code": 500}

    @staticmethod
    def query_refund(args):
        """
        查询退款状态

        参数:
            args: 包含查询条件的字典，需要包含 out_refund_no (商户退款单号)

        返回:
            包含退款信息的字典
        """
        # 获取查询参数
        out_refund_no = args.get("out_refund_no")  # 商户退款单号

        if not out_refund_no:
            return {"error": "缺少商户退款单号", "code": 400}

        # 初始化微信支付客户端
        wxpay = init_wechat_pay()
        if not wxpay:
            return {"error": "微信支付初始化失败", "code": 500}

        try:
            # 调用微信支付查询退款API
            code, message = wxpay.query_refund(out_refund_no=out_refund_no)

            result = json.loads(message)
            if code in range(200, 300):
                # 查询成功，返回退款信息
                return {
                    "data": result,
                    "code": 200
                }
            else:
                # 查询失败，返回错误信息
                return {
                    "error": result.get("message", "退款查询失败"),
                    "code": code
                }

        except Exception as e:
            current_app.logger.error(f"查询退款异常: {str(e)}")
            return {"error": f"查询退款异常: {str(e)}", "code": 500}

    @staticmethod
    def close_order(args):
        """
        关闭订单

        参数:
            args: 包含订单信息的字典，需要包含 out_trade_no (商户订单号)

        返回:
            包含关闭结果的字典
        """
        # 获取订单参数
        out_trade_no = args.get("out_trade_no")  # 商户订单号

        if not out_trade_no:
            return {"error": "缺少商户订单号", "code": 400}

        # 获取配置
        config = get_config()
        mchid = config['MCHID']

        # 初始化微信支付客户端
        wxpay = init_wechat_pay()
        if not wxpay:
            return {"error": "微信支付初始化失败", "code": 500}

        try:
            # 调用微信支付关闭订单API
            code, message = wxpay.close(
                out_trade_no=out_trade_no,
                mchid=mchid
            )

            result = json.loads(message) if message else {}
            if code in range(200, 300):
                # 关闭成功，返回结果
                return {
                    "data": result,
                    "code": 200,
                    "message": "订单关闭成功"
                }
            else:
                # 关闭失败，返回错误信息
                return {
                    "error": result.get("message", "订单关闭失败"),
                    "code": code
                }

        except Exception as e:
            current_app.logger.error(f"关闭订单异常: {str(e)}")
            return {"error": f"关闭订单异常: {str(e)}", "code": 500}

    @staticmethod
    def wx_withdrawal(args):
        wxpay = init_wechat_pay()
        if not wxpay:
            return {"error": "微信支付初始化失败", "code": 500}
        out_bill_no = "OUTBATCH20250528221953297245"
        transfer_remark = "测试转账"
        transfer_amount = 40
        transfer_scene_id = "1005"
        openid = "od-Km7eh_iuz-f8qUhjQ2OfJtGwM"
        notify_url = "https://dwjc.mcorg.com/api/v1/wx_mini_app/shop_pay/wx_pay_notify"
        user_name = "肖飞"
        user_recv_perception = "劳务报酬"
        transfer_scene_report_infos = [{
    "info_type" :   "岗位类型",
    "info_content" : "销售"
},{
    "info_type" : "报酬说明",
    "info_content" : "测试的佣金费用"
}]
        data = wxpay.mch_transfer_bills(out_bill_no=out_bill_no, transfer_scene_id=transfer_scene_id,
                                        openid=openid, transfer_amount=transfer_amount, transfer_remark=transfer_remark,
                                        user_recv_perception=user_recv_perception, user_name=user_name,
                                        notify_url=notify_url, transfer_scene_report_infos=transfer_scene_report_infos

                                        )
        print(data)
