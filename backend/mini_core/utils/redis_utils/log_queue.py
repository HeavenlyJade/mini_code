# backend/mini_core/utils/redis_utils/log_queue.py

import json
import datetime as dt
from typing import Dict, Any, Optional
from flask import request

from backend.extensions import redis


class LogQueue:
    """用户操作日志队列处理类"""

    LOG_QUEUE_KEY = "user_operation_logs"

    @classmethod
    def push_log_dict(cls, log_dict: Dict[str, Any]) -> bool:
        """
        直接推送日志字典到队列

        Args:
            log_dict: 包含 op_type 和 data 的日志字典

        Returns:
            bool: 是否成功推送
        """
        # 验证日志结构是否正确
        if 'op_type' not in log_dict or 'data' not in log_dict:
            print("日志结构错误: 缺少 op_type 或 data 字段")
            return False

        # 确保日期时间对象正确序列化
        prepared_data = cls._prepare_data_for_json(log_dict)

        try:
            # 使用Redis客户端的push_data方法将日志推送到队列
            redis.push_data(cls.LOG_QUEUE_KEY, prepared_data)
            return True
        except Exception as e:
            print(f"推送日志到队列失败: {str(e)}")
            return False

    @classmethod
    def add_order_log(cls,
                      order_no: str,
                      operation_type: str,
                      operation_desc: str,
                      operator: str,
                      old_value: Any = None,
                      new_value: Any = None,
                      operation_time: dt.datetime = None,
                      remark: str = None,
                      updater: str = None) -> bool:
        """
        添加订单操作日志到队列

        Args:
            order_no: 订单编号
            operation_type: 操作类型
            operation_desc: 操作描述
            operator: 操作人
            old_value: 修改前值 (可选)
            new_value: 修改后值 (可选)
            operation_time: 操作时间 (可选，默认为当前时间)
            remark: 备注 (可选)
            updater: 更新人 (可选，默认为操作人)

        Returns:
            bool: 是否成功添加到队列
        """
        # 构建内部日志数据
        create_log_dict = {
            'order_no': order_no,
            'operation_type': operation_type,
            'operation_desc': operation_desc,
            'operator': operator,
            'operation_time': operation_time or dt.datetime.now(),
            'updater': updater or operator
        }

        # 添加可选字段
        if old_value is not None:
            create_log_dict['old_value'] = old_value

        if new_value is not None:
            create_log_dict['new_value'] = new_value

        if remark:
            create_log_dict['remark'] = remark

        # 添加客户端IP (如果在请求上下文中)
        client_ip = cls._get_client_ip()
        if client_ip:
            create_log_dict['operation_ip'] = client_ip

        # 构建外层包装 - 使用 op_type 和 data 结构
        create_log_dic = {
            'op_type': "order",
            'data': create_log_dict
        }

        return cls.push_log_dict(create_log_dic)

    @classmethod
    def add_return_log(cls,
                       return_id: int,
                       return_no: str,
                       operation_type: str,
                       operation_desc: str,
                       operator: str,
                       new_status: Optional[str] = None,
                       old_status: Optional[str] = None,
                       operation_time: dt.datetime = None,
                       remark: str = None,
                       updater: str = None) -> bool:
        """
        添加退货操作日志到队列

        Args:
            return_id: 退货单ID
            return_no: 退货单号
            operation_type: 操作类型
            operation_desc: 操作描述
            operator: 操作人
            new_status: 新状态 (可选)
            old_status: 旧状态 (可选)
            operation_time: 操作时间 (可选，默认为当前时间)
            remark: 备注 (可选)
            updater: 更新人 (可选，默认为操作人)

        Returns:
            bool: 是否成功添加到队列
        """
        # 构建内部日志数据
        return_logs_dict = {
            'return_id': return_id,
            'return_no': return_no,
            'operation_type': operation_type,
            'operation_desc': operation_desc,
            'operator': operator,
            'operation_time': operation_time or dt.datetime.now(),
            'updater': updater or operator
        }

        # 添加可选字段
        if new_status is not None:
            return_logs_dict['new_status'] = new_status

        if old_status is not None:
            return_logs_dict['old_status'] = old_status

        if remark:
            return_logs_dict['remark'] = remark

        # 添加客户端IP (如果在请求上下文中)
        client_ip = cls._get_client_ip()
        if client_ip:
            return_logs_dict['operation_ip'] = client_ip

        # 构建外层包装 - 使用 op_type 和 data 结构
        return_logs_dic = {
            'op_type': "return_order",
            'data': return_logs_dict
        }

        return cls.push_log_dict(return_logs_dic)

    @classmethod
    def _prepare_data_for_json(cls, data: Any) -> Any:
        """
        预处理数据以便JSON序列化，主要处理datetime对象

        Args:
            data: 任意数据

        Returns:
            处理后的数据
        """
        if isinstance(data, dt.datetime):
            return data.isoformat()
        elif isinstance(data, dict):
            return {k: cls._prepare_data_for_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls._prepare_data_for_json(item) for item in data]
        else:
            return data

    @staticmethod
    def _get_client_ip() -> str:
        """获取客户端IP地址"""
        if not request:
            return ""

        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr or ""
