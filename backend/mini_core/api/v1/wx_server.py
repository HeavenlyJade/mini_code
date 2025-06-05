from flask.views import MethodView

from backend.business.service.auth import auth_required

from backend.mini_core.service.shop_app.wx_server_new import WechatPayService

from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('wx_server', 'wx_server', url_prefix='/wx_server')

#
# @blp.route('/wx_withdrawal')
# class WxWithdrawal(MethodView):
#     """ 分销数据初始化"""
#
#     @blp.response()
#     def get(self, ):
#         """微信的接口"""
#         result = WechatPayService.wx_withdrawal({})
#         return result
