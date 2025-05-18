import uuid
import json
import datetime as dt
from typing import Dict, Any, List, Optional
from flask import request, g
from flask_jwt_extended import get_current_user
from decimal import Decimal
from flask_jwt_extended import current_user

from kit.domain.entity import Entity
from kit.service.base import CRUDService
from backend.mini_core.domain.order.order_return import OrderReturn, OrderReturnDetail, OrderReturnLog
from backend.mini_core.repository.order.order_return_sql import OrderReturnSQLARepository, \
    OrderReturnDetailSQLARepository, OrderReturnLogSQLARepository
from backend.mini_core.service.order.order_detail import OrderDetailService

__all__ = ['OrderReturnService', 'OrderReturnDetailService', 'OrderReturnLogService']


class OrderReturnService(CRUDService[OrderReturn]):
    def __init__(self, repo: OrderReturnSQLARepository, detail_service:OrderReturnDetailSQLARepository,
                 log_service:OrderReturnLogSQLARepository):
        super().__init__(repo)
        self._repo = repo
        self._detail_service = detail_service
        self._log_service = log_service

    @property
    def repo(self) -> OrderReturnSQLARepository:
        return self._repo

    @property
    def order_detail_service(self) -> OrderDetailService:
        from backend.mini_core.service import order_detail_service
        return order_detail_service

    def get_return_list(self, args: dict) -> Dict[str, Any]:
        """获取退货单列表"""
        # 处理时间范围查询
        if 'start_time' in args and 'end_time' in args:
            args['apply_time'] = [args.pop('start_time'), args.pop('end_time')]

        if 'audit_start_time' in args and 'audit_end_time' in args:
            args['audit_time'] = [args.pop('audit_start_time'), args.pop('audit_end_time')]

        if 'complete_start_time' in args and 'complete_end_time' in args:
            args['complete_time'] = [args.pop('complete_start_time'), args.pop('complete_end_time')]

        # 处理金额范围查询
        if 'min_amount' in args and 'max_amount' in args:
            args['return_amount'] = [args.pop('min_amount'), args.pop('max_amount')]

        data, total = self._repo.list(**args)
        return dict(data=data, code=200, total=total)

    def get_return_by_order_no(self, order_no: str) -> Dict[str, Any]:
        """通过ID获取退货单详情信息"""
        return_data = self._repo.find(**{"order_no": order_no}) # 退货订单数据
        if not return_data:
            return dict(data=None, code=404, message="退货单不存在")

        # 获取退货商品明细
        details = self._detail_service.get_return_details(order_no)

        # 获取操作日志
        logs = self._log_service.get_return_logs(return_data.return_no)

        return dict(
            data={
                "return_info": return_data,
                "return_details": details,
                "return_logs": logs
            },
            code=200
        )

    def get_return_by_no(self, return_no: str) -> Dict[str, Any]:
        """通过退货单号获取退货单"""
        return_data = self._repo.get_by_return_no(return_no)
        if not return_data:
            return dict(data=None, code=404, message="退货单不存在")

        return self.get_return_by_id(return_data.id)

    def get_returns_by_order(self, order_no: str) -> Dict[str, Any]:
        """获取订单相关的所有退货单"""
        returns = self._repo.get_by_order_no(order_no)
        return dict(data=returns, code=200, total=len(returns))

    def get_user_returns(self, user_id: int) -> Dict[str, Any]:
        """获取用户的所有退货单"""
        returns = self._repo.get_user_returns(user_id)
        return dict(data=returns, code=200, total=len(returns))

    def get_return_stats(self) -> Dict[str, Any]:
        """获取退货统计信息"""
        stats = self._repo.get_return_stats()
        return dict(data=stats, code=200)

    def get_monthly_stats(self) -> Dict[str, Any]:
        """获取月度退货统计"""
        data = self._repo.get_monthly_stats()
        return dict(data=data, code=200)

    def create_return(self, application) -> Dict[str, Any]:
        """
        创建退货单及其商品明细
        从订单表和订单详情表获取数据，处理客户的退货/退款申请

        参数:
            application: 退货申请信息，包含订单号、退货原因和要退货的商品列表

        返回:
            包含创建结果的字典
        """
        from backend.mini_core.service import shop_order_service
        order_no = application.get('order_no')
        return_reason = application.get('reason', '客户申请退货')
        return_detail = application.get('return_detail', [])

        # 从订单表获取订单信息
        order_result = shop_order_service.get_order_by_order_no(order_no)
        if order_result.get('code') != 200 or not order_result.get('data'):
            return dict(code=404, message="订单不存在")
        order = order_result.get('data')

        # 验证是否已经存在该订单的退货单
        existing_return = self._repo.find(order_no=order_no)
        if existing_return:
            return dict(code=400, message="该订单已有退货申请，请勿重复提交")

        # 获取订单详情信息
        order_details = self.order_detail_service.get_order_details(order_no)
        if not order_details or not order_details.get('order_details'):
            return dict(code=404, message="订单商品信息不存在")

        # 生成退货单号
        now = dt.datetime.now()
        return_no = f"RT{now.strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"

        # 获取当前用户
        current_user = get_current_user()
        username = current_user.username if hasattr(current_user, 'username') else 'customer'

        # 将订单详情转换为可查询的字典
        order_detail_dict = {}
        for detail in order_details.get('order_details', []):
            order_detail_dict[detail['order_item_id']] = detail

        # 准备退货单数据
        return_data = {
            'return_no': return_no,
            'order_no': order_no,
            'user_id': order.user_id,
            'return_type': '退货退款',  # 默认为退货退款
            'return_reason': return_reason,
            'status': 0,  # 设置为待审核状态
            'apply_time': now,
            'updater': username,
            'process_username': username
        }

        # 计算退款总金额和总数量
        total_amount = Decimal('0')
        total_quantity = 0

        # 准备退货商品详情
        detail_items = []
        for item in return_detail:
            order_item_id = item.get('order_item_id')
            if not order_item_id or order_item_id not in order_detail_dict:
                return dict(code=400, message=f"商品明细ID不存在于订单中: {order_item_id}")

            order_detail = order_detail_dict[order_item_id]

            # 默认退货数量等于原订单购买数量
            quantity = order_detail.get('num', 1)

            # 计算小计金额
            item_price = Decimal(str(order_detail.get('actual_price', 0)))
            item_subtotal = item_price * quantity

            # 构建退货明细数据
            detail_item = {
                'return_no': return_no,
                'order_item_id': order_item_id,
                'order_no': order_no,
                'product_id': order_detail.get('product_id'),
                'sku_id': order_detail.get('sku_id'),
                'product_name': order_detail.get('product_name'),
                'product_img': order_detail.get('product_img'),
                'product_spec': order_detail.get('product_spec'),
                'price': item_price,
                'quantity': quantity,
                'subtotal': item_subtotal,
                'reason': return_reason
            }

            detail_items.append(detail_item)
            total_amount += item_subtotal
            total_quantity += quantity

        # 设置退款总金额和数量
        return_data['return_amount'] = total_amount
        return_data['return_quantity'] = total_quantity
        re_data = self._repo.create_return_transaction(return_data, detail_items, order_no,username)
        # 如果事务执行成功，处理日志
        if re_data.get('code') == 200:
            from backend.mini_core.message.shop_user import ReturnStatusMapping
            from backend.mini_core.utils.redis_utils.log_queue import LogQueue

            status_text = ReturnStatusMapping.get_status_text(0)  # 获取"待审核"状态的文本描述
            new_value_status= ReturnStatusMapping.get_status_data_text(0)
            create_log_dict ={
                    'order_no': order_no,
                    "old_value":dict(status="已付款",),
                    "new_value":dict(status=new_value_status,),
                    'operation_type': "申请退货",
                    'operation_desc': f"用户申请退货，原因：{return_reason}，退款金额：{total_amount}",
                    'operator': username,
                    'operation_time': now,

                }
            create_log_dic=dict(op_type="order",data=create_log_dict)
            return_logs_dict ={
                    'return_no': return_no,
                    'operation_type': '申请退货',
                    'operation_desc': f'用户:{username},订单号:{return_no},申请退货退款，原因：{return_reason}，退款金额：{total_amount}',
                    'operator': username,
                    'operation_time': now,
                    'new_status': status_text,
                    # "updater":username,
                }
            from backend.mini_core.utils.base import get_client_ip
            client_ip = get_client_ip()
            if client_ip:
                return_logs_dict['operation_ip'] = client_ip
            return_logs_dic = dict(op_type="return_order",data=return_logs_dict)
            LogQueue.push_log_dict(create_log_dic)
            LogQueue.push_log_dict(return_logs_dic)
        return re_data


    def update_return_status(self, order_no: str, status: str, **kwargs) -> Dict[str, Any]:
        from backend.mini_core.message.shop_user import ReturnStatusMapping
        from backend.mini_core.service import  order_return_log_service
        """更新退货单状态"""
        return_obj = self._repo.find(order_no=order_no)
        if not return_obj:
            return dict(data=None, code=404, message="退货单不存在")

        old_status = return_obj.status
        if old_status == status:
            return dict(data=return_obj, code=200, message="状态未发生变化")

        # 更新退货单状态

        # 记录操作日志
        current_user = get_current_user()
        operator = current_user.username if hasattr(current_user, 'username') else 'system'

        operation_type = ReturnStatusMapping.get_operation_type(status)
        status_text = ReturnStatusMapping.get_status_text(status)  # 返回 '已拒绝'
        old_status_text  = ReturnStatusMapping.get_status_text(old_status)  # 返回 '已拒绝'
        operation_desc = f'退货单状态从"{old_status_text}"变更为"{status_text}"'
        if status_text == '已拒绝' and 'refuse_reason' in kwargs:
            operation_desc += f'，拒绝原因：{kwargs["refuse_reason"]}'
        order_return_log_service.create_log({
            'return_no': return_obj.return_no,
            'operation_type': operation_type,
            'operation_desc': operation_desc,
            'operator': operator,
            'operation_time': dt.datetime.now(),
            'old_status': old_status_text,
            'new_status': status_text,
            'remark': kwargs.get('admin_remark')
        })
        result = self._repo.update_status(order_no, status, **kwargs)

        return dict(data=result, code=200, message=f"退货单状态已更新为{status}")

    def update_shipping_info(self, return_id: int, express_company: str, express_no: str) -> Dict[str, Any]:
        """更新退货单的物流信息"""
        return_obj = self._repo.get_by_id(return_id)
        if not return_obj:
            return dict(data=None, code=404, message="退货单不存在")

        if return_obj.status != '已同意':
            return dict(data=None, code=400, message="当前状态不允许更新物流信息")

        # 更新物流信息
        return_obj.return_express_company = express_company
        return_obj.return_express_no = express_no
        self._repo.update(return_id, return_obj)

        # 记录操作日志
        current_user = get_current_user()
        operator = current_user.username if hasattr(current_user, 'username') else 'system'

        self._log_service.create_log({
            'return_id': return_id,
            'return_no': return_obj.return_no,
            'operation_type': '物流信息更新',
            'operation_desc': f'用户更新退货单物流信息，快递公司：{express_company}，快递单号：{express_no}',
            'operator': operator,
            'operation_time': dt.datetime.now(),
            'old_status': return_obj.status,
            'new_status': return_obj.status
        })

        # 如果是用户上传了物流信息，可能需要将状态更新为待收货
        if return_obj.return_type == '退货退款':
            self.update_return_status(return_id, '退款中')

        return dict(data=return_obj, code=200, message="物流信息更新成功")

    def _get_client_ip(self) -> str:
        """获取客户端IP地址"""
        if not request:
            return ""

        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr or ""


class OrderReturnDetailService(CRUDService[OrderReturnDetail]):
    def __init__(self, repo: OrderReturnDetailSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> OrderReturnDetailSQLARepository:
        return self._repo

    def get_return_details(self, return_id: int) -> list[Entity]:
        """获取退货单的所有商品明细"""
        return self._repo.get_return_details(return_id)

    def get_product_returns(self, product_id: int) -> Dict[str, Any]:
        """获取指定商品的所有退货记录"""
        details = self._repo.get_product_returns(product_id)
        return dict(data=details, code=200, total=len(details))

    def create_details(self, details: List[OrderReturnDetail]) -> None:
        """批量创建退货商品明细"""
        self._repo.create_details(details)


class OrderReturnLogService(CRUDService[OrderReturnLog]):
    def __init__(self, repo: OrderReturnLogSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> OrderReturnLogSQLARepository:
        return self._repo

    def get_return_logs(self, return_id: int) -> List[OrderReturnLog]:
        """获取退货单的所有操作日志"""
        return self._repo.get_return_logs(return_id)

    def get_return_logs_by_no(self, return_no: str) -> Dict[str, Any]:
        """通过退货单号获取所有操作日志"""
        logs = self._repo.get_return_logs_by_no(return_no)
        return dict(data=logs, code=200, total=len(logs))

    def get_operator_logs(self, operator: str) -> Dict[str, Any]:
        """获取指定操作员的所有操作日志"""
        logs = self._repo.get_operator_logs(operator)
        return dict(data=logs, code=200, total=len(logs))

    def create_log(self, log_data: Dict[str, Any]) -> OrderReturnLog:
        """创建退货单操作日志"""
        # 设置操作时间
        if 'operation_time' not in log_data or not log_data['operation_time']:
            log_data['operation_time'] = dt.datetime.now()
        log = OrderReturnLog(**log_data)
        return self.create(log)
