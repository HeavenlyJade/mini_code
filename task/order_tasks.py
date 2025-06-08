import datetime as dt
from typing import List, Dict, Any
from celery import current_app
from task import celery
from celery.signals import worker_ready
from backend.mini_core.repository import shop_order_sqla_repo
from backend.mini_core.service import shop_order_service
from backend.mini_core.utils.redis_utils.log_queue import LogQueue
from loguru import logger

@celery.task(name='auto_complete_delivered_orders')
def auto_complete_delivered_orders():
    """
    自动完成已发货订单的定时任务
    查找发货状态为"已发货"且transaction_time在最近14天内且payment_no存在的订单
    将其状态变更为"已完成"并奖励积分
    """
    try:
        # 计算14天前的时间
        fourteen_days_ago = dt.datetime.now() - dt.timedelta(days=14)

        # 查询条件
        query_conditions = {
            'delivery_status': '已发货',
            'transaction_time': [fourteen_days_ago, dt.datetime.now()],
            'payment_no__isnull': False  # payment_no 不为空
        }

        # 调用Repository层方法查询符合条件的订单
        orders = shop_order_sqla_repo.get_and_complete_delivered_orders(fourteen_days_ago)

        if not orders:
            LogQueue.add_system_log(
                operation_type='定时任务',
                operation_desc='自动完成订单任务执行完成，未找到符合条件的订单',
                operator='system'
            )
            return {
                'status': 'success',
                'message': '未找到符合条件的订单',
                'processed_count': 0,
                'total_found': 0
            }

        success_count = 0
        failed_count = 0
        failed_orders = []
        total_found = len(orders)

        # 批量处理订单
        for order in orders:
            try:
                # 准备更新数据
                order_update_data = {
                    'delivery_status': '已签收',
                    'status': '已完成',
                    'confirm_time': dt.datetime.now(),
                    'updater': 'system'
                }

                # 计算积分奖励
                actual_amount = order.actual_amount or 0
                points_reward = float(actual_amount)

                # 获取用户当前积分
                from backend.mini_core.repository import shop_user_sqla_repo
                user = shop_user_sqla_repo.find(user_id=order.user_id)
                if not user:
                    failed_count += 1
                    failed_orders.append({
                        'order_no': order.order_no,
                        'reason': '用户不存在'
                    })
                    continue

                original_points = user.points or 0
                new_points = original_points + points_reward

                user_update_data = {
                    'points': new_points
                }

                # 调用Repository层方法完成订单
                result = shop_order_sqla_repo.confirm_receipt_with_points(
                    order.order_no, order_update_data, user_update_data
                )

                if result.get('code') == 200:
                    success_count += 1

                    # 记录成功日志
                    LogQueue.add_order_log(
                        order_no=order.order_no,
                        operation_type='自动完成订单',
                        operation_desc=f'系统自动完成订单，奖励积分 {points_reward} 分',
                        operator='system',
                        old_value={
                            'order_status': '已发货',
                            'delivery_status': '已发货',
                            'user_points': original_points
                        },
                        new_value={
                            'order_status': '已完成',
                            'delivery_status': '已签收',
                            'user_points': new_points
                        },
                        remark=f'定时任务自动处理，支付金额：{actual_amount}元'
                    )
                else:
                    failed_count += 1
                    failed_orders.append({
                        'order_no': order.order_no,
                        'reason': result.get('message', '未知错误')
                    })

            except Exception as e:
                failed_count += 1
                failed_orders.append({
                    'order_no': order.order_no,
                    'reason': f'处理异常: {str(e)}'
                })

        # 记录任务执行结果

        return None

    except Exception as e:
        error_msg = f'自动完成订单任务执行失败: {str(e)}'

        return {
            'status': 'error',
            'message': error_msg,
            'processed_count': 0
        }

@celery.task(name='manual_trigger_auto_complete_orders')
def manual_trigger_auto_complete_orders():
    """手动触发自动完成订单任务"""
    logger.info("订单任务开始执行")
    return auto_complete_delivered_orders.apply_async()


@worker_ready.connect
def start_logistics_task(sender, **kwargs):
    logger.info("订单任务开始执行")
    return auto_complete_delivered_orders.delay()

