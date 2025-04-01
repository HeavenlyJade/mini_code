import datetime as dt
from typing import Optional, List, Dict, Any
import json
from flask import request, g

from kit.service.base import CRUDService
from backend.mini_core.domain.order.order_log import OrderLog
from backend.mini_core.repository.order.order_log_sql import OrderLogSQLARepository

__all__ = ['OrderLogService']


class OrderLogService(CRUDService[OrderLog]):
    def __init__(self, repo: OrderLogSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> OrderLogSQLARepository:
        return self._repo

    def get_order_logs(self, order_no: str) -> Dict[str, Any]:
        """获取指定订单的所有操作日志"""
        logs = self._repo.get_order_logs(order_no)
        return dict(data=logs, code=200, total=len(logs))

    def get_order_logs_by_type(self, order_no: str, operation_type: str) -> Dict[str, Any]:
        """获取指定订单的指定类型的操作日志"""
        logs = self._repo.get_order_logs_by_type(order_no, operation_type)
        return dict(data=logs, code=200, total=len(logs))

    def get_operator_logs(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """获取指定操作人的操作日志"""
        operator = args.get('operator')
        start_time = args.get('start_time')
        end_time = args.get('end_time')

        logs = self._repo.get_operator_logs(operator, start_time, end_time)
        return dict(data=logs, code=200, total=len(logs))

    def get_latest_logs(self, limit: int = 50) -> Dict[str, Any]:
        """获取最新的操作日志"""
        logs = self._repo.get_latest_logs(limit)
        return dict(data=logs, code=200, total=len(logs))

    def search_logs(self, search_term: str) -> Dict[str, Any]:
        """搜索操作日志"""
        logs = self._repo.search_logs(search_term)
        return dict(data=logs, code=200, total=len(logs))

    def get_statistics(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """获取操作日志统计数据"""
        start_time = args.get('start_time')
        end_time = args.get('end_time')

        stats = self._repo.get_statistics(start_time, end_time)
        return dict(data=stats, code=200)

    def create_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建操作日志"""
        # 如果未提供操作时间，则使用当前时间
        if 'operation_time' not in log_data or not log_data['operation_time']:
            log_data['operation_time'] = dt.datetime.now()

        # 如果未提供操作IP，尝试从请求中获取
        if 'operation_ip' not in log_data or not log_data['operation_ip']:
            log_data['operation_ip'] = self._get_client_ip()

        # 如果未提供更新人，尝试从g对象中获取
        if 'updater' not in log_data or not log_data['updater']:
            if hasattr(g, 'creator'):
                log_data['updater'] = g.creator

        # 将old_value和new_value转换为JSON字符串(如果是字典)
        if 'old_value' in log_data and isinstance(log_data['old_value'], dict):
            log_data['old_value'] = json.dumps(log_data['old_value'])

        if 'new_value' in log_data and isinstance(log_data['new_value'], dict):
            log_data['new_value'] = json.dumps(log_data['new_value'])

        log = OrderLog(**log_data)
        result = self.create(log)
        return dict(data=result, code=200)

    def batch_create_logs(self, logs_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量创建操作日志"""
        log_objects = []

        for log_data in logs_data:
            # 如果未提供操作时间，则使用当前时间
            if 'operation_time' not in log_data or not log_data['operation_time']:
                log_data['operation_time'] = dt.datetime.now()

            # 如果未提供操作IP，尝试从请求中获取
            if 'operation_ip' not in log_data or not log_data['operation_ip']:
                log_data['operation_ip'] = self._get_client_ip()

            # 如果未提供更新人，尝试从g对象中获取
            if 'updater' not in log_data or not log_data['updater']:
                if hasattr(g, 'creator'):
                    log_data['updater'] = g.creator

            # 将old_value和new_value转换为JSON字符串(如果是字典)
            if 'old_value' in log_data and isinstance(log_data['old_value'], dict):
                log_data['old_value'] = json.dumps(log_data['old_value'])

            if 'new_value' in log_data and isinstance(log_data['new_value'], dict):
                log_data['new_value'] = json.dumps(log_data['new_value'])

            log_objects.append(OrderLog(**log_data))

        self._repo.create_many(log_objects)
        return dict(code=200, message=f"成功创建{len(log_objects)}个操作日志")

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

    def log_order_action(self, order_no: str, operation_type: str, operation_desc: str,
                         operator: str, old_value: Dict = None, new_value: Dict = None,
                         remark: str = None) -> OrderLog:
        """记录订单操作日志的便捷方法"""
        log_data = {
            'order_no': order_no,
            'operation_type': operation_type,
            'operation_desc': operation_desc,
            'operator': operator,
            'operation_time': dt.datetime.now(),
            'operation_ip': self._get_client_ip(),
            'old_value': json.dumps(old_value) if old_value else None,
            'new_value': json.dumps(new_value) if new_value else None,
            'remark': remark,
            'updater': operator
        }

        log = OrderLog(**log_data)
        return self.create(log)
