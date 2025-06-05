from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_current_user

from backend.business.service.auth import auth_required
from backend.mini_core.domain.distributionWithdrawal import DistributionWithdrawal
from backend.mini_core.schema.distribution_withdrawal import (
    DistributionWithdrawalSchema,
    DistributionWithdrawalQueryArgSchema,
    DistributionWithdrawalCreateSchema,
    DistributionWithdrawalUpdateSchema,DistributionWithdrawalDetailResponseSchema,
    DistributionWithdrawalListSchema
)
from backend.mini_core.service import distribution_withdrawal_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('distribution_withdrawal', 'distribution_withdrawal', url_prefix='/distribution_withdrawal')


@blp.route('/withdraw')
class MyWithdrawalAPI(MethodView):
    """当前用户提现申请API"""

    decorators = [jwt_required()]

    @blp.arguments(DistributionWithdrawalQueryArgSchema, location='query')
    @blp.response(DistributionWithdrawalListSchema)
    def get(self, args: dict):
        """查看当前用户的提现申请列表"""
        current_user = get_current_user()
        user_id = str(current_user.user_id)
        return distribution_withdrawal_service.get_user_withdrawal_list(user_id, args)

    @blp.arguments(DistributionWithdrawalCreateSchema)
    @blp.response(DistributionWithdrawalDetailResponseSchema)
    def post(self, withdrawal_data: dict):
        """当前用户申请提现"""
        current_user = get_current_user()
        withdrawal_data['user_id'] = str(current_user.user_id)
        withdrawal_data["openid"]  = current_user.openid
        withdrawal_data["user_name"] = current_user.username
        re_data = distribution_withdrawal_service.apply_withdrawal(withdrawal_data)
        return re_data
