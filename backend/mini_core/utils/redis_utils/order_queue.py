import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from backend.extensions import redis


class RedisOrderQueue:
    """
    基于Redis的待支付订单队列管理
    """

    # Redis键前缀
    PENDING_ORDERS_KEY = "pending_orders"
    ORDER_DATA_KEY_PREFIX = "order_data:"
    ORDER_EXPIRY_INDEX = "order_expiry_index"

    # 默认过期时间（30分钟）
    DEFAULT_EXPIRY_SECONDS = 30 * 60

    @classmethod
    def add_pending_order(cls, order_no: str, order_data: Dict[str, Any],
                          expire_seconds: int = DEFAULT_EXPIRY_SECONDS) -> bool:
        """
        添加订单到待支付队列

        参数:
            order_no: 订单号
            order_data: 订单数据，应包含:
                - id: 订单ID
                - user_id: 用户ID
                - actual_amount: 订单实际金额
                - product_amount: 订单商品金额
                - product_count: 商品数量
                - status: 订单状态
                - payment_status: 支付状态
            expire_seconds: 过期时间（秒），默认30分钟

        返回:
            bool: 是否添加成功
        """
        from backend.extensions import redis
        import json
        import time

        try:
            # 验证必要的订单字段
            required_fields = [ 'user_id', 'actual_amount', 'product_amount',
                               'product_count', 'status', 'payment_status']

            for field in required_fields:
                if field not in order_data:
                    print(f"订单数据缺少必要字段: {field}")
                    return False

            # 确保只存储必要的数据（减少Redis空间使用）
            order_storage_data = {
                'user_id': order_data['user_id'],
                'order_no': order_no,
                'actual_amount': str(order_data['actual_amount']),  # 转为字符串，避免Decimal序列化问题
                'product_amount': str(order_data['product_amount']),
                'product_count': order_data['product_count'],
                'status': order_data['status'],
                'payment_status': order_data['payment_status'],
                'create_time': order_data.get('create_time', int(time.time())),
                'expire_time': int(time.time()) + expire_seconds
            }

            # 计算过期时间戳
            expiry_time = int(time.time()) + expire_seconds

            # 存储订单数据（带过期时间）
            order_data_key = f"{cls.ORDER_DATA_KEY_PREFIX}{order_no}"

            # 使用 RedisHook 的 set_key_with_expiration 方法替代 setex
            redis.set_key_with_expiration(order_data_key, json.dumps(order_storage_data), expire_seconds)

            # 添加到待支付订单集合
            redis.client.sadd(cls.PENDING_ORDERS_KEY, order_no)

            # 添加到过期时间有序集合（用于快速查找即将过期的订单）
            redis.client.zadd(cls.ORDER_EXPIRY_INDEX, {order_no: expiry_time})

            return True
        except Exception as e:
            print(f"添加订单到待支付队列出错: {str(e)}")
            return False

    @classmethod
    def remove_pending_order(cls, order_no: str) -> bool:
        """
        从待支付队列中移除订单

        参数:
            order_no: 订单号

        返回:
            bool: 是否移除成功
        """
        from backend.extensions import redis

        try:
            # 从待支付订单集合中移除
            redis.client.srem(cls.PENDING_ORDERS_KEY, order_no)

            # 从过期时间索引中移除
            redis.client.zrem(cls.ORDER_EXPIRY_INDEX, order_no)

            # 删除订单数据
            order_data_key = f"{cls.ORDER_DATA_KEY_PREFIX}{order_no}"
            redis.client.delete(order_data_key)

            return True
        except Exception as e:
            print(f"从待支付队列移除订单出错: {str(e)}")
            return False

    @classmethod
    def get_order_data(cls, order_no: str) -> Optional[Dict[str, Any]]:
        """
        获取订单数据

        参数:
            order_no: 订单号

        返回:
            Dict或None: 订单数据，如果不存在则返回None
        """
        from backend.extensions import redis
        import json

        try:
            order_data_key = f"{cls.ORDER_DATA_KEY_PREFIX}{order_no}"
            data = redis.client.get(order_data_key)

            if data:
                # RedisHook 已设置 decode_responses=True，所以不需要再解码
                return json.loads(data)
            return None
        except Exception as e:
            print(f"获取订单数据出错: {str(e)}")
            return None

    @classmethod
    def get_expiring_orders(cls, within_seconds: int = 300) -> List[str]:
        """
        获取即将过期的订单

        参数:
            within_seconds: 即将过期的时间范围（秒），默认5分钟

        返回:
            List[str]: 即将过期的订单号列表
        """
        from backend.extensions import redis
        import time

        try:
            current_time = int(time.time())
            max_time = current_time + within_seconds

            # 获取即将过期的订单
            expiring_orders = redis.client.zrangebyscore(
                cls.ORDER_EXPIRY_INDEX,
                current_time,
                max_time
            )

            # RedisHook 已设置 decode_responses=True，所以不需要再解码
            return expiring_orders
        except Exception as e:
            print(f"获取即将过期订单出错: {str(e)}")
            return []

    @classmethod
    def get_all_pending_orders(cls) -> List[str]:
        """
        获取所有待支付订单

        返回:
            List[str]: 所有待支付订单号列表
        """
        try:
            pending_orders = redis.smembers(cls.PENDING_ORDERS_KEY)

            # 如果返回的是字节类型，转换为字符串
            return [order.decode() if isinstance(order, bytes) else order
                    for order in pending_orders]
        except Exception as e:
            print(f"获取所有待支付订单出错: {str(e)}")
            return []

    @classmethod
    def cleanup_expired_orders(cls) -> int:
        """
        清理过期订单

        返回:
            int: 清理的订单数量
        """
        try:
            current_time = int(time.time())

            # 获取已过期订单
            expired_orders = redis.zrangebyscore(
                cls.ORDER_EXPIRY_INDEX,
                0,
                current_time
            )

            # 如果返回的是字节类型，转换为字符串
            expired_order_nos = [order.decode() if isinstance(order, bytes) else order
                                 for order in expired_orders]

            cleaned_count = 0
            for order_no in expired_order_nos:
                # 处理过期订单（更新数据库中的状态）
                cls._handle_expired_order(order_no)

                # 从Redis中移除
                cls.remove_pending_order(order_no)
                cleaned_count += 1

            return cleaned_count
        except Exception as e:
            print(f"清理过期订单出错: {str(e)}")
            return 0

    @classmethod
    def _handle_expired_order(cls, order_no: str) -> None:
        """
        处理过期订单（例如在数据库中取消）

        参数:
            order_no: 过期的订单号
        """
        try:
            # 导入服务（避免循环导入）
            from backend.mini_core.service import shop_order_service

            # 根据订单号获取订单
            order_result = shop_order_service.get_order_by_order_no(order_no)

            if order_result and order_result.get('code') == 200 and order_result.get('data'):
                order = order_result['data']

                # 如果订单仍处于"待支付"状态，则关闭它
                if order.status == '待支付' and order.payment_status == '待支付':
                    shop_order_service.close_order(order.id)

                    # 记录自动关闭日志
                    from backend.mini_core.service import order_log_service
                    order_log_service.create_log({
                        'order_no': order_no,
                        'operation_type': '系统自动关闭',
                        'operation_desc': '订单支付超时，系统自动关闭',
                        'operator': 'system',
                    })
        except Exception as e:
            print(f"处理过期订单 {order_no} 出错: {str(e)}")

    @classmethod
    def get_remaining_seconds(cls, order_no: str) -> Optional[int]:
        """
        获取订单剩余支付时间（秒）

        参数:
            order_no: 订单号

        返回:
            int或None: 剩余秒数，如果订单不存在则返回None
        """
        try:
            # 从过期时间索引中获取过期时间
            expiry_time = redis.zscore(cls.ORDER_EXPIRY_INDEX, order_no)

            if expiry_time is None:
                return None

            # 计算剩余时间
            remaining = int(expiry_time - time.time())
            return max(0, remaining)  # 不返回负值
        except Exception as e:
            print(f"获取订单剩余时间出错: {str(e)}")
            return None
