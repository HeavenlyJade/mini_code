"""Custom Redis Hook."""
import time, uuid, json
from typing import List, Optional

from flask import Flask
from loguru import logger
from redis import ConnectionError, StrictRedis
from redis.sentinel import Sentinel
from rediscluster import ClusterBlockingConnectionPool, RedisCluster

from kit.exceptions import ServiceConfigException
from kit.hook.base import BaseHook
from kit.message import ExtensionMessage


class RedisHook(BaseHook):
    """Redis hook to interact with redis server"""

    def __init__(self, app: Flask = None):
        self.app: Optional[Flask] = app
        self.client = None
        self.raw_client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask, redis_conn_name: str = 'redis_default'):


        self.app = app
        connection_kwargs = dict(
            socket_timeout=0.5, retry_on_timeout=True, socket_keepalive=True
        )
        redis_url = app.config['REDIS_URL']
        if password := app.config.get('REDIS_PASSWORD'):
            connection_kwargs['password'] = password
            # 如果 URL 中没有密码，添加密码
            if ':@' not in redis_url:
                redis_url = redis_url.replace('redis://', f'redis://:{password}@')
        self.client = StrictRedis.from_url(redis_url, decode_responses=True, **connection_kwargs)
        self.raw_client = StrictRedis.from_url(redis_url, **connection_kwargs)
        logger.info(f'Initializing redis hook for conn_name {redis_conn_name}')
        self._detect_connectivity()
    # def init_app(self, app: Flask, redis_conn_name: str = 'redis_default'):
    #     self.app = app
    #     connection_kwargs = dict(
    #         socket_timeout=0.5, retry_on_timeout=True, socket_keepalive=True
    #     )
    #     print("app.config.get('REDIS_PASSWORD')",app.config.get('REDIS_PASSWORD'))
    #     if password := app.config.get('REDIS_PASSWORD'):
    #         connection_kwargs['password'] = password
    #
    #     if redis_cluster_nodes := app.config.get('REDIS_CLUSTER_NODES'):
    #         startup_nodes = self._get_rc_startup_nodes(redis_cluster_nodes)
    #         connection_pool = ClusterBlockingConnectionPool(
    #             startup_nodes, **connection_kwargs
    #         )
    #         self.client = RedisCluster(
    #             connection_pool=connection_pool, decode_responses=True
    #         )
    #         self.raw_client = RedisCluster(connection_pool=connection_pool)
    #     elif sentinel_nodes := app.config.get('REDIS_SENTINEL_NODES'):
    #         sentinels = self._get_sentinel_nodes(sentinel_nodes)
    #         sentinel = Sentinel(sentinels, decode_responses=True, **connection_kwargs)
    #         raw_sentinel = Sentinel(sentinels, **connection_kwargs)
    #         self.client = sentinel.master_for('mymaster', **connection_kwargs)
    #         self.raw_client = raw_sentinel.master_for('mymaster', **connection_kwargs)
    #     else:
    #         redis_url = app.config['REDIS_URL']
    #         self.client = StrictRedis.from_url(
    #             redis_url, decode_responses=True, **connection_kwargs
    #         )
    #         self.raw_client = StrictRedis.from_url(redis_url, **connection_kwargs)
    #     logger.info(f'Initializing redis hook for conn_name {redis_conn_name}')
    #     self._detect_connectivity()

    @staticmethod
    def _get_sentinel_nodes(sentinel_nodes: List[str]) -> List[tuple]:
        start_up_nodes = list()
        for node in sentinel_nodes:
            host, port = node.split(':')
            start_up_nodes.append((host, port))
        return start_up_nodes

    @staticmethod
    def _get_rc_startup_nodes(redis_cluster_nodes: List[str]) -> List[dict]:
        start_up_nodes = list()
        for node in redis_cluster_nodes:
            host, port = node.split(':')
            start_up_nodes.append(dict(host=host, port=port))
        return start_up_nodes

    def _detect_connectivity(self):
        try:
            self.client.ping()
        except ConnectionError:
            raise ServiceConfigException(ExtensionMessage.REDIS_CONNECT_ERROR)

    def acquire_lock(self, lock_name: str, acquire_time=5, time_out=5):
        """获取一个分布式锁"""
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_time
        lock = f"string:lock:{lock_name}"
        while time.time() < end:
            if self.client.setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                self.client.expire(lock, time_out)
                return identifier
            elif not self.client.ttl(lock):
                self.client.expire(lock, time_out)
            time.sleep(0.001)
        return False

    def release_lock(self, lock_name: str, identifier: str):
        """释放锁"""
        lock = f"string:lock:{lock_name}"
        pip = self.client.pipeline(True)
        while True:
            try:
                pip.watch(lock)
                lock_value = self.client.get(lock)
                if not lock_value:
                    return True
                if not isinstance(lock_value, str):
                    lock_value = lock_value.decode
                if lock_value == identifier:
                    pip.multi()
                    pip.delete(lock)
                    pip.execute()
                    return True
                pip.unwatch()
                break
            except ServiceConfigException:
                pass
        return False

    def set_key_with_expiration(self, key_name, value, exp_time=1800):
        self.client.setex(key_name, exp_time, value)

    def push_data(self, queue_name: str, msg: dict):
        from backend.rtr.utils import datetime_handler
        return self.client.lpush(queue_name, json.dumps(msg, default=datetime_handler))

    def pop_data(self, queue_name):
        return self.client.rpop(queue_name)
