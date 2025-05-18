# 在 backend/mini_core/utils/__init__.py 或 datetime_utils.py 中

import datetime
import decimal


def datetime_handler(obj):
    """
    处理 JSON 序列化无法处理的类型，主要用于日期时间类型

    Args:
        obj: 需要序列化的对象

    Returns:
        可序列化的形式（通常是字符串）

    Raises:
        TypeError: 当无法处理传入类型时抛出
    """
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    # 可能还会处理其他类型...

    # 如果无法处理，抛出类型错误
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def get_client_ip() -> str:
    """
    获取当前请求的客户端IP地址

    依次尝试从以下来源获取IP:
    1. X-Forwarded-For 头 (通常由代理/负载均衡器添加)
    2. X-Real-IP 头 (通常由 Nginx 添加)
    3. request.remote_addr (直接连接的客户端地址)

    Returns:
        str: 客户端IP地址，如果无法获取则返回空字符串
    """
    from flask import request

    if not request:
        return ""

    # 检查 X-Forwarded-For 头
    if request.headers.get('X-Forwarded-For'):
        # 取第一个地址，因为这是最初的客户端IP
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()

    # 检查 X-Real-IP 头
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')

    # 使用 remote_addr 作为后备选项
    else:
        return request.remote_addr or ""
