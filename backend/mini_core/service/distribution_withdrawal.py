from decimal import Decimal
from typing import Dict, Any

from backend.mini_core.domain.distributionWithdrawal import DistributionWithdrawal
from backend.mini_core.repository.distribution.withdrawal_application import DistributionWithdrawalSQLARepository
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService


class DistributionWithdrawalService(CRUDService[DistributionWithdrawal]):
    def __init__(self, repo: DistributionWithdrawalSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DistributionWithdrawalSQLARepository:
        return self._repo

    def apply_withdrawal(self, withdrawal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建提现申请并更新分销用户的待提现金额
        使用事务确保数据一致性

        Args:
            withdrawal_data: 提现申请数据，包含:
                - user_id: 用户ID
                - user_name:用户名称
                - apply_amount: 申请提现金额
                - withdrawal_type: 提现方式
                - account_info: 收款账户信息(dict格式)
                - remark: 备注(可选)

        Returns:
            Dict: 包含创建结果的字典
        """
        return self.repo.create_withdrawal_with_distribution_update(withdrawal_data)

    def audit_withdrawal(self, withdrawal_id: int, status: int,
                         handler_id: int, handler_name: str,
                         reject_reason: str = None) -> Dict[str, Any]:
        """审核提现申请"""

        from backend.mini_core.service.shop_app.wx_server_new import WechatPayService
        from backend.mini_core.service import shop_user_service
        # WechatPayService.
        withdrawal_data = self._repo.get_by_id(withdrawal_id)

        if not withdrawal_data or withdrawal_data.status != 0:
            raise ServiceBadRequest("提现申请不存在或状态不正确")
        withdrawal_user_id = withdrawal_data.user_id
        user_data = shop_user_service.find(user_id=withdrawal_user_id, )
        if not user_data or not user_data.openid:
            raise ServiceBadRequest("申请的用户不存在")
        withdrawal_no = withdrawal_data.withdrawal_no
        withdrawal_openid = user_data.openid
        withdrawal_user_name = user_data.username
        transfer_amount = int(float(withdrawal_data.apply_amount) * 100)
        transfer_data = dict(openid=withdrawal_openid, username=withdrawal_user_name, out_bill_no=withdrawal_no,
                             transfer_amount=transfer_amount)
        args_wi_data = dict(status=status, handler_id=handler_id, handler_name=handler_name,
                            withdrawal_id=withdrawal_no, reject_reason=reject_reason)

        if status == 1:
            code, res = WechatPayService.wx_withdrawal(args=transfer_data)
            if code != 200:
                message = res["message"]
                raise ServiceBadRequest(message)
            else:
                transfer_bill_no = res["transfer_bill_no"]
                wx_state = res["state"]
                args_wi_data["transfer_bill_no"] = transfer_bill_no
                args_wi_data["wx_state"] = wx_state

        return self.repo.audit_withdrawal_with_distribution_update(withdrawal_data,args_wi_data)

    def complete_withdrawal(self, withdrawal_id: int, transaction_id: str,
                            actual_amount: Decimal = None, fee_amount: Decimal = None) -> Dict[str, Any]:
        """完成提现"""
        return self.repo.complete_withdrawal_with_distribution_update(
            withdrawal_id, transaction_id, actual_amount, fee_amount
        )

    def get_withdrawal_list(self, args: dict) -> Dict[str, Any]:
        """
        查询所有提现申请单

        Args:
            args: 查询参数，包含以下可选字段:
                - user_id: 用户ID
                - status: 状态筛选
                - withdrawal_type: 提现方式
                - handler_id: 处理人ID
                - start_time: 开始时间
                - end_time: 结束时间
                - withdrawal_no: 提现单号
                - page: 页码
                - size: 每页数量
                - ordering: 排序字段

        Returns:
            Dict: 包含提现申请列表和总数的字典
        """
        if 'start_time' in args and 'end_time' in args:
            args['apply_time'] = [args.pop('start_time'), args.pop('end_time')]

        # 设置默认排序（最新申请在前）
        if 'ordering' not in args:
            args['ordering'] = ['-apply_time']

        # 启用总数统计
        args['need_total_count'] = True

        # 调用仓储层的 list 方法
        data, total = self.repo.list(**args)
        return {
            'code': 200,
            'data': data,
            'total': total,
            'message': '查询成功'
        }

    def get_user_withdrawal_list(self, user_id: str, args: dict = None) -> Dict[str, Any]:
        """
        查询指定用户的提现申请列表

        Args:
            user_id: 用户ID
            args: 其他查询参数（可选）

        Returns:
            Dict: 包含用户提现申请列表的字典
        """
        if args is None:
            args = {}

        # 设置用户ID
        args['user_id'] = user_id

        return self.get_withdrawal_list(args)
