# task/order_log/user_log_processor.py

import json
import datetime as dt
import time
from typing import Dict, Any, List
from loguru import logger

from task import celery
from backend.extensions import redis
from celery.signals import worker_ready

@celery.task(bind=True)
def redis_log_consumer(self, queue_key="user_operation_logs", wait_time=1):
    """
    持续监听 Redis 队列并消费日志消息

    Args:
        queue_key: Redis 队列键名
        wait_time: 队列为空时等待的秒数

    Returns:
        None - 这个任务会持续运行，直到被终止
    """
    from backend.mini_core.service import order_log_service
    from backend.mini_core.service import order_return_log_service

    logger.info(f"开始监听 Redis 队列 '{queue_key}'")

    # 处理日志消息的统计信息
    stats = {
        "total_processed": 0,
        "order_logs_processed": 0,
        "return_logs_processed": 0,
        "errors": 0,
        "start_time": dt.datetime.now().isoformat()
    }

    # 上次打印统计信息的时间
    last_stats_time = dt.datetime.now()

    try:
        # 持续监听队列
        while True:
            # 从 Redis 队列中获取一条消息
            log_data = redis.client.rpop(queue_key)
            if log_data:
                # 处理消息
                try:
                    if isinstance(log_data, bytes):
                        log_data = log_data.decode('utf-8')

                    log_entry = json.loads(log_data)

                    # 从日志条目中提取操作类型和数据
                    op_type = log_entry.get('op_type', '')
                    log_data = log_entry.get('data', {})

                    # 处理时间字段
                    if 'operation_time' in log_data and isinstance(log_data['operation_time'], str):
                        try:
                            log_data['operation_time'] = dt.datetime.fromisoformat(log_data['operation_time'])
                        except ValueError:
                            log_data['operation_time'] = dt.datetime.now()

                    # 根据操作类型分别处理
                    if op_type == "return_order":
                        # 退货日志
                        order_return_log_service.create_log(log_data)
                        stats["return_logs_processed"] += 1
                        logger.info(f"已处理退货日志: {log_data.get('return_no', 'N/A')}")
                    elif op_type == "order":
                        # 订单日志
                        order_log_service.create_log(log_data)
                        stats["order_logs_processed"] += 1
                        logger.info(f"已处理订单日志: {log_data.get('order_no', 'N/A')}")
                    else:
                        # 未知类型日志
                        logger.warning(f"未知日志类型: {op_type}")
                        stats["errors"] += 1

                    stats["total_processed"] += 1

                except Exception as e:
                    logger.error(f"处理日志消息出错: {str(e)}")
                    stats["errors"] += 1
            else:
                # 队列为空，等待一段时间
                time.sleep(wait_time)

            # 每分钟打印一次统计信息
            now = dt.datetime.now()
            if (now - last_stats_time).total_seconds() > 60:
                logger.info(f"日志处理统计: 总计: {stats['total_processed']}, "
                            f"订单日志: {stats['order_logs_processed']}, "
                            f"退货日志: {stats['return_logs_processed']}, "
                            f"错误: {stats['errors']}")
                last_stats_time = now

    except Exception as e:
        logger.error(f"消费者任务异常终止: {str(e)}")
        # 如果任务异常终止，重新启动
        raise self.retry(exc=e, countdown=5)


@worker_ready.connect
def start_consumer(sender, **kwargs):
    """
    当 Celery Worker 启动完成后，自动启动消费者任务
    """
    logger.info("Worker 准备就绪，启动 Redis 日志消费者任务")
    redis_log_consumer.delay()
