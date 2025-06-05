import datetime as dt
from typing import Type, Tuple, List, Dict, Any, Optional
from decimal import Decimal
from sqlalchemy import Column, String, Table, Integer, DECIMAL, Text, DateTime, and_, or_, desc, func
from sqlalchemy.orm import aliased
from kit.exceptions import ServiceBadRequest
from sqlalchemy.exc import SQLAlchemyError
import uuid
import json
from backend.extensions import mapper_registry
from backend.mini_core.domain.distributionWithdrawal import DistributionWithdrawal
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['DistributionWithdrawalSQLARepository']

# 提现申请表
withdrawal_table = Table(
    'la_distribution_withdrawal',
    mapper_registry.metadata,
    id_column(),
    Column('user_id', String(50), comment='用户ID'),
    Column('user_name', String(50), comment='用户名称'),
    Column('withdrawal_no', String(50), unique=True, comment='提现申请单号'),
    Column('apply_amount', DECIMAL(10, 2), comment='申请提现金额'),
    Column('actual_amount', DECIMAL(10, 2), comment='实际到账金额'),
    Column('fee_amount', DECIMAL(10, 2), default=0, comment='手续费'),
    Column('withdrawal_type', String(20), comment='提现方式(微信/支付宝/银行卡)'),
    Column('account_info', Text, comment='收款账户信息(JSON格式)'),
    Column('status', Integer, default=0, comment='状态(0:待审核,1:审核通过,2:审核拒绝,3:处理中,4:已完成,5:失败)'),
    Column('apply_time', DateTime, comment='申请时间'),
    Column('audit_time', DateTime, comment='审核时间'),
    Column('process_time', DateTime, comment='处理时间'),
    Column('complete_time', DateTime, comment='完成时间'),
    Column('handler_id', Integer, comment='处理人ID'),
    Column('handler_name', String(50), comment='处理人姓名'),
    Column('reject_reason', String(255), comment='拒绝原因'),
    Column('remark', String(255), comment='备注'),
    Column('transaction_id', String(100), comment='第三方交易流水号'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

# 映射关系
mapper_registry.map_imperatively(DistributionWithdrawal, withdrawal_table)


class DistributionWithdrawalSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[DistributionWithdrawal]:
        return DistributionWithdrawal

    @property
    def query_params(self) -> Tuple:
        return ('user_id', 'withdrawal_no', 'status', 'withdrawal_type', 'handler_id')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('handler_name', 'transaction_id', 'remark')

    @property
    def range_query_params(self) -> Tuple:
        return ('apply_time', 'audit_time', 'process_time', 'complete_time', 'apply_amount', 'actual_amount')

    def create_withdrawal_with_distribution_update(self, withdrawal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建提现申请并更新分销用户的待提现金额
        使用事务确保数据一致性

        Args:
            withdrawal_data: 提现申请数据，包含:
                - user_id: 用户ID
                - apply_amount: 申请提现金额
                - withdrawal_type: 提现方式
                - account_info: 收款账户信息(dict格式)
                - remark: 备注(可选)

        Returns:
            Dict: 包含创建结果的字典
        """
        try:
            # 1. 获取分销用户信息
            from backend.mini_core.repository.distribution.distribution_sqla import DistributionSQLARepository
            distribution_repo = DistributionSQLARepository(self.session)

            user_id = withdrawal_data.get('user_id')
            user_name = withdrawal_data.get("user_name")
            distribution = distribution_repo.find(user_id=user_id)

            if not distribution:
                raise ServiceBadRequest("分销用户不存在")

            # 2. 检查可提现金额
            apply_amount = Decimal(str(withdrawal_data.get('apply_amount', 0)))
            current_wait_amount = Decimal(str(distribution.wait_amount or 0))


            # 3. 生成提现申请单号
            withdrawal_no = self._generate_withdrawal_no()

            # 4. 创建提现申请记录
            withdrawal = DistributionWithdrawal(
                user_id=user_id,
                user_name =user_name,
                withdrawal_no=withdrawal_no,
                apply_amount=apply_amount,
                withdrawal_type=withdrawal_data.get('withdrawal_type'),
                account_info=json.dumps(withdrawal_data.get('account_info', {})),
                status=0,  # 待审核
                apply_time=dt.datetime.now(),
                remark=withdrawal_data.get('remark')
            )

            # 5. 保存提现申请
            created_withdrawal = self.create(withdrawal,commit=False)

            # 6. 更新分销用户的待提现金额（从待提现金额中扣除）
            distribution.wait_amount = current_wait_amount - apply_amount
            distribution_repo.update(distribution.id, distribution)

            # 7. 记录分销日志（可选）
            self._create_withdrawal_log(distribution.id, apply_amount, withdrawal_no, "申请提现")
            self.session.commit()
            return {
                'code': 200,
                'data': created_withdrawal,
                'message': '提现申请提交成功',
                'withdrawal_no': withdrawal_no
            }

        except ServiceBadRequest as e:
            # 业务异常，回滚事务
            self.session.rollback()
            return {
                'code': 400,
                'data': None,
                'message': str(e)
            }
        except SQLAlchemyError as e:
            # 数据库异常，回滚事务
            self.session.rollback()
            return {
                'code': 500,
                'data': None,
                'message': f'数据库操作失败: {str(e)}'
            }
        except Exception as e:
            # 其他异常，回滚事务
            self.session.rollback()
            return {
                'code': 500,
                'data': None,
                'message': f'系统错误: {str(e)}'
            }

    def audit_withdrawal_with_distribution_update(self,withdrawal,args_wi_data) -> Dict[str, Any]:
        """
        审核提现申请并更新分销用户金额
        如果审核拒绝，将金额退回到待提现金额

        Args:
            withdrawal_id: 提现申请ID
            status: 审核状态 (1:审核通过, 2:审核拒绝)
            handler_id: 处理人ID
            handler_name: 处理人姓名
            reject_reason: 拒绝原因（审核拒绝时必填）

        Returns:
            Dict: 包含审核结果的字典
        """
        print("withdrawal,args_wi_data",withdrawal,args_wi_data)
        try:
            # 2. 更新提现申请状态
            status = args_wi_data["status"]
            withdrawal_id = withdrawal.id
            reject_reason = args_wi_data["reject_reason"]
            withdrawal_user_id =args_wi_data["withdrawal_user_id"]
            withdrawal.status = status
            withdrawal.audit_time = dt.datetime.now()
            withdrawal.handler_id = args_wi_data["handler_id"]

            withdrawal.handler_name = args_wi_data["handler_name"]
            if status == 2:  # 审核拒绝
                withdrawal.reject_reason = reject_reason
                # 3. 如果审核拒绝，退回金额到待提现
                from backend.mini_core.repository.distribution.distribution_sqla import DistributionSQLARepository
                distribution_repo = DistributionSQLARepository(self.session)
                distribution = distribution_repo.find(user_id=withdrawal_user_id)
                if distribution:
                    current_wait_amount = Decimal(str(distribution.wait_amount or 0))
                    distribution.wait_amount = current_wait_amount + withdrawal.apply_amount
                    distribution_repo.update(distribution.id, distribution)
                    # 记录退回日志
                    self._create_withdrawal_log(
                        distribution.id,
                        withdrawal.apply_amount,
                        withdrawal.withdrawal_no,
                        f"审核拒绝退回金额，原因: {reject_reason}"
                    )
            elif status == 1:
                withdrawal.transaction_id = args_wi_data["transfer_bill_no"]

            # 4. 保存更新
            updated_withdrawal = self.update(withdrawal_id, withdrawal)

            status_text = "审核通过" if status == 1 else "审核拒绝"
            return {
                'code': 200,
                'data': updated_withdrawal,
                'message': f'提现申请{status_text}'
            }

        except ServiceBadRequest as e:
            self.session.rollback()
            return {
                'code': 400,
                'data': None,
                'message': str(e)
            }
        except Exception as e:
            print(e)
            self.session.rollback()
            return {
                'code': 500,
                'data': None,
                'message': f'审核失败: {str(e)}'
            }

    def complete_withdrawal_with_distribution_update(self, withdrawal_id: int,
                                                     transaction_id: str,
                                                     actual_amount: Decimal = None,
                                                     fee_amount: Decimal = None) -> Dict[str, Any]:
        """
        完成提现并更新分销用户已提现金额

        Args:
            withdrawal_id: 提现申请ID
            transaction_id: 第三方交易流水号
            actual_amount: 实际到账金额（可选，默认为申请金额）
            fee_amount: 手续费（可选）

        Returns:
            Dict: 包含完成结果的字典
        """
        try:
            with self.session.begin():
                # 1. 获取提现申请
                withdrawal = self.get_by_id(withdrawal_id)
                if not withdrawal or withdrawal.status not in [1, 3]:  # 审核通过或处理中
                    raise ServiceBadRequest("提现申请状态不正确")

                # 2. 计算实际金额和手续费
                if actual_amount is None:
                    actual_amount = withdrawal.apply_amount
                if fee_amount is None:
                    fee_amount = withdrawal.apply_amount - actual_amount

                # 3. 更新提现申请
                withdrawal.status = 4  # 已完成
                withdrawal.complete_time = dt.datetime.now()
                withdrawal.transaction_id = transaction_id
                withdrawal.actual_amount = actual_amount
                withdrawal.fee_amount = fee_amount

                # 4. 更新分销用户的已提现金额
                from backend.mini_core.repository.distribution.distribution_sqla import DistributionSQLARepository
                distribution_repo = DistributionSQLARepository(self.session)

                distribution = distribution_repo.get_by_id(withdrawal.distribution_id)
                if distribution:
                    current_withdrawn_amount = Decimal(str(distribution.withdrawn_amount or 0))
                    distribution.withdrawn_amount = current_withdrawn_amount + actual_amount
                    distribution_repo.update(distribution.id, distribution)

                    # 记录完成日志
                    self._create_withdrawal_log(
                        distribution.id,
                        actual_amount,
                        withdrawal.withdrawal_no,
                        f"提现完成，实际到账: {actual_amount}，手续费: {fee_amount}"
                    )

                # 5. 保存更新
                updated_withdrawal = self.update(withdrawal_id, withdrawal)

                return {
                    'code': 200,
                    'data': updated_withdrawal,
                    'message': '提现完成'
                }

        except ServiceBadRequest as e:
            self.session.rollback()
            return {
                'code': 400,
                'data': None,
                'message': str(e)
            }
        except Exception as e:
            self.session.rollback()
            return {
                'code': 500,
                'data': None,
                'message': f'提现完成失败: {str(e)}'
            }

    def _generate_withdrawal_no(self) -> str:
        """生成提现申请单号"""
        now = dt.datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4().int)[:6]
        return f"WD{timestamp}{random_str}"

    def _create_withdrawal_log(self, distribution_id: int, amount: Decimal,
                               withdrawal_no: str, action: str) -> None:
        """创建提现相关的分销日志"""
        try:
            from backend.mini_core.repository.distribution.distribution_sqla import DistributionLogSQLARepository
            from backend.mini_core.domain.distribution import DistributionLog

            log_repo = DistributionLogSQLARepository(self.session)

            log = DistributionLog(
                distribution_id=distribution_id,
                change_object="wait_amount",
                change_type="提现",
                action=action,
                source_sn=withdrawal_no,
                create_time=dt.datetime.now()
            )

            log_repo.create(log)
        except Exception as e:
            # 日志创建失败不影响主流程
            print(f"创建提现日志失败: {str(e)}")



