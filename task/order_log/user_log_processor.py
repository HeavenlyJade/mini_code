# order_log/user_log_processor.py

import json
import datetime as dt
from typing import Dict, Any, List
from loguru import logger

from task import celery
from backend.extensions import redis


@celery.task(name="tasks.order_log.process_user_operation_logs")
def process_user_operation_logs(queue_key="user_operation_logs", batch_size=100):
    """
    从Redis队列读取用户操作日志，并根据日志类型分别写入不同的日志表

    Args:
        queue_key: Redis队列键名
        batch_size: 每批处理的日志数量

    Returns:
        dict: 处理统计信息
    """
    from backend.mini_core.service import order_log_service
    from backend.mini_core.service import order_return_log_service

    # 初始化统计信息
    stats = {
        "total_processed": 0,
        "order_logs_processed": 0,
        "return_logs_processed": 0,
        "errors": 0,
        "start_time": dt.datetime.now().isoformat(),
        "end_time": None
    }

    logger.info(f"开始从Redis队列 '{queue_key}' 处理用户操作日志")

    # 从Redis队列获取日志
    logs_to_process = []

    for _ in range(batch_size):
        log_data = redis.client.rpop(queue_key)
        if not log_data:
            # 队列为空，结束循环
            break

        # 解析日志数据
        try:
            if isinstance(log_data, bytes):
                log_data = log_data.decode('utf-8')

            log_entry = json.loads(log_data)
            logs_to_process.append(log_entry)
        except Exception as e:
            logger.error(f"解析日志数据出错: {str(e)}, 数据: {log_data}")
            stats["errors"] += 1

    # 处理日志
    for log_entry in logs_to_process:
        try:
            # 从日志条目中提取操作类型和数据
            op_type = log_entry.get('op_type', '')
            log_data = log_entry.get('data', {})
            # 处理时间字段
            if 'operation_time' in log_data and isinstance(log_data['operation_time'], str):
                try:
                    # 尝试解析ISO格式的时间字符串
                    log_data['operation_time'] = dt.datetime.fromisoformat(log_data['operation_time'])
                except ValueError:
                    # 如果解析失败，使用当前时间
                    log_data['operation_time'] = dt.datetime.now()

            # 根据操作类型分别处理
            if op_type == "return_order":
                # 退货日志 - 使用data字段中的数据直接传递给服务
                order_return_log_service.create_log(log_data)
                stats["return_logs_processed"] += 1
            elif op_type == "order":
                # 订单日志 - 使用data字段中的数据直接传递给服务
                order_log_service.create_log(log_data)
                stats["order_logs_processed"] += 1
            else:
                # 未知类型日志
                logger.warning(f"未知日志类型: {op_type}, 数据: {log_data}")
                stats["errors"] += 1
                continue

            stats["total_processed"] += 1

        except Exception as e:
            logger.error(f"处理日志条目时出错: {str(e)}, 日志: {log_entry}")
            stats["errors"] += 1

    # 更新统计结果
    stats["end_time"] = dt.datetime.now().isoformat()
    duration = dt.datetime.fromisoformat(stats["end_time"]) - dt.datetime.fromisoformat(stats["start_time"])
    stats["duration_seconds"] = duration.total_seconds()

    logger.info(f"日志处理完成. 总计: {stats['total_processed']}, "
                f"订单日志: {stats['order_logs_processed']}, "
                f"退货日志: {stats['return_logs_processed']}, "
                f"错误: {stats['errors']}")

    return stats
