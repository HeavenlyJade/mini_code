from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_current_user

from backend.business.service.auth import auth_required
from backend.mini_core.domain.distributionWithdrawal import DistributionWithdrawal
from backend.mini_core.schema.distribution_withdrawal import (
    DistributionWithdrawalSchema,
    DistributionWithdrawalQueryArgSchema,
    DistributionWithdrawalListSchema,
    DistributionWithdrawalUpdateSchema,

)
from backend.mini_core.service import distribution_withdrawal_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('distribution_withdrawal', 'distribution_withdrawal', url_prefix='/distribution_withdrawal')

@blp.route('/view')
class DistributionWithdrawalViewList(MethodView):
    decorators = [auth_required()]

    @blp.arguments(DistributionWithdrawalQueryArgSchema)
    @blp.response(DistributionWithdrawalListSchema)
    def get(self,args):
        return distribution_withdrawal_service.get_withdrawal_list(args)
@blp.route('/<int:withdrawal_id>')
class DistributionWithdrawalByIDAPI(MethodView):
    """单个提现申请管理API"""

    decorators = [auth_required()]

    @blp.response(DistributionWithdrawalSchema)
    def get(self, withdrawal_id: int):
        """提现管理 查看提现申请详情"""
        withdrawal = distribution_withdrawal_service.get(withdrawal_id)
        return dict(data=withdrawal, code=200)

    @blp.arguments(DistributionWithdrawalUpdateSchema)
    @blp.response(DistributionWithdrawalSchema)
    def put(self, withdrawal_data: dict, withdrawal_id: int):
        """提现管理 更新提现申请"""
        result = distribution_withdrawal_service.update(withdrawal_id, DistributionWithdrawal(**withdrawal_data))
        return dict(data=result, code=200)


@blp.route('/audit/<int:withdrawal_id>')
class WithdrawalAuditAPI(MethodView):
    """提现申请审核API"""

    decorators = [auth_required()]

    @blp.arguments(DistributionWithdrawalUpdateSchema)
    @blp.response(DistributionWithdrawalSchema)
    def put(self, audit_data: dict, withdrawal_id: int):
        """审核提现申请"""
        current_user = get_current_user()
        handler_id = current_user.id
        handler_name = current_user.username

        status = audit_data.get('status')
        reject_reason = audit_data.get('reject_reason')

        return distribution_withdrawal_service.audit_withdrawal(
            withdrawal_id, status, handler_id, handler_name, reject_reason
        )

@blp.route('/complete/<int:withdrawal_id>')
class WithdrawalCompleteAPI(MethodView):
    """提现申请完成API"""

    decorators = [auth_required()]

    @blp.arguments(DistributionWithdrawalUpdateSchema)
    @blp.response(DistributionWithdrawalSchema)
    def put(self, complete_data: dict, withdrawal_id: int):
        """完成提现申请"""
        transaction_id = complete_data.get('transaction_id')
        actual_amount = complete_data.get('actual_amount')
        fee_amount = complete_data.get('fee_amount')

        return distribution_withdrawal_service.complete_withdrawal(
            withdrawal_id, transaction_id, actual_amount, fee_amount
        )
