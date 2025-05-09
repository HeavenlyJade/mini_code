from flask.views import MethodView
from flask import request, jsonify
import json

from backend.mini_core.schema.shop_app.wx_pay import WxPay,WxPaySchema
from backend.mini_core.service.shop_app.wx_server import WechatPayService
from backend.business.service.auth import auth_required
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('shop_pay', 'shop_pay', url_prefix='/shop_pay')
@blp.route('/wx_shop_pay', methods=['POST'])
class WxShopPay(MethodView):
    """微信支付"""
    decorators = [auth_required()]

    @blp.arguments(WxPay)
    @blp.response(WxPaySchema)
    def post(self, args, user_id):
        """创建微信支付订单"""
        # 调用支付服务创建订单
        result = WechatPayService.create_jsapi_order(args)
        return result

@blp.route('/wx_pay_notify', methods=['POST'])
class WxPayNotify(MethodView):
    """微信支付回调接口"""

    def post(self):
        """
        接收微信支付通知
        需要验证签名，解密数据，更新订单状态
        """

        # 获取请求头中的签名信息
        wechatpay_timestamp = request.headers.get('Wechatpay-Timestamp')
        wechatpay_nonce = request.headers.get('Wechatpay-Nonce')
        wechatpay_signature = request.headers.get('Wechatpay-Signature')
        wechatpay_serial = request.headers.get('Wechatpay-Serial')

        # 获取请求体数据
        notify_data = request.data

        # 验证签名，解密数据
        if not WechatPayService.verify_notify_signature(
            wechatpay_timestamp,
            wechatpay_nonce,
            notify_data,
            wechatpay_signature,
            wechatpay_serial
        ):
            return jsonify({
                "code": "FAIL",
                "message": "签名验证失败"
            }), 401

        # 解析请求体数据
        data = json.loads(notify_data)

        # 解密数据
        decrypted_data = WechatPayService.decrypt_notify_data(data.get('resource', {}))

        # 处理支付结果
        result = WechatPayService.process_payment_result(decrypted_data)

        # 根据处理结果返回响应
        if result.get('success'):
            # 成功处理，返回成功响应
            return jsonify({
                "code": "SUCCESS",
                "message": "成功"
            })
        else:
            # 处理失败，返回失败响应
            return jsonify({
                "code": "FAIL",
                "message": result.get('error', '处理失败')
            }), 500





