# mypy: no-strict-optional
import uuid
import json
import logging
from typing import Optional
from threading import Thread, Lock, Event

from casbin import Enforcer
from casbin.model import Model
from casbin.persist.adapter import Adapter
from casbin_sqlalchemy_adapter import Adapter as SQLAdapter
from flask import Flask, current_app
from loguru import logger
from redis import Redis
from redis.client import Redis, PubSub

from kit.exceptions import ServiceConfigException
from kit.message import ExtensionMessage

__all__ = ['CasbinEnforcer']


class WatcherOptions:
    sub_client = None
    pub_client = None
    channel = None
    ignore_self = None
    local_ID = None
    optional_update_callback = None

    def init_config(self) -> None:
        if self.local_ID is None:
            self.local_ID = str(uuid.uuid4())

        if self.channel is None:
            self.channel = '/casbin'


class RedisWatcher:
    def __init__(self, redis_cli: Redis) -> None:
        self.mutex: Lock = Lock()
        self.redis_cli: Redis = redis_cli
        self.sub_client: Optional[PubSub] = None
        self.pub_client: Optional[Redis] = None
        self.options: Optional[WatcherOptions] = None
        self.close = None
        self.callback: callable = None
        self.subscribe_thread: Thread = Thread(target=self.subscribe, daemon=True)
        self.subscribe_event = Event()
        self.logger = logging.getLogger(__name__)

    def init_config(self, options: WatcherOptions):
        if options.optional_update_callback:
            self.set_update_callback(options.optional_update_callback)
        else:
            self.logger.warning('No callback function is set. Use the default callback function.')
            self.callback = self.default_callback_func

        self.options = options

    def set_update_callback(self, callback: callable) -> None:
        with self.mutex:
            self.callback = callback

    def update(self) -> None:
        def func():
            with self.mutex:
                msg = MSG('Update', self.options.local_ID, '', '', '')
                return self.pub_client.publish(self.options.channel, msg.marshal_binary())

        return self.log_record(func)

    def update_for_add_policy(self, sec: str, ptype: str, *params: str):
        def func():
            with self.mutex:
                msg = MSG('UpdateForAddPolicy', self.options.local_ID, sec, ptype, params)
                return self.pub_client.publish(self.options.channel, msg.marshal_binary())

        return self.log_record(func)

    def update_for_remove_policy(self, sec: str, ptype: str, *params: str):
        def func():
            with self.mutex:
                msg = MSG('UpdateForRemovePolicy', self.options.local_ID, sec, ptype, params)
                return self.pub_client.publish(self.options.channel, msg.marshal_binary())

        return self.log_record(func)

    def update_for_remove_filtered_policy(self, sec: str, ptype: str, field_index: int, *params: str):
        def func():
            with self.mutex:
                msg = MSG(
                    'UpdateForRemoveFilteredPolicy',
                    self.options.local_ID,
                    sec,
                    ptype,
                    f"{field_index} {' '.join(params)}",
                )
                return self.pub_client.publish(self.options.channel, msg.marshal_binary())

        return self.log_record(func)

    def update_for_save_policy(self, model: Model):
        def func():
            with self.mutex:
                msg = MSG(
                    'UpdateForSavePolicy',
                    self.options.local_ID,
                    '',
                    '',
                    model.to_text(),
                )
                return self.pub_client.publish(self.options.channel, msg.marshal_binary())

        return self.log_record(func)

    @staticmethod
    def default_callback_func(msg: str):
        logger.debug('callback: ' + msg)

    @staticmethod
    def log_record(f: callable):
        try:
            result = f()
        except Exception as e:
            logger.warning(f'Casbin Redis Watcher error: {e}')
        else:
            return result

    @staticmethod
    def unsubscribe(psc: PubSub):
        return psc.unsubscribe()

    def subscribe(self):
        self.sub_client.subscribe(self.options.channel)
        for item in self.sub_client.listen():
            if not self.subscribe_event.is_set():
                self.subscribe_event.set()
            if item is not None and item['type'] == 'message':
                with self.mutex:
                    self.callback(str(item))


class MSG:
    def __init__(self, method: str = '', id_: str = '', sec: str = '', ptype: str = '', *params):
        self.method: str = method
        self.id_: str = id_
        self.sec: str = sec
        self.ptype: str = ptype
        self.params = params

    def marshal_binary(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def unmarshal_binary(data: bytes) -> 'MSG':
        loaded = json.loads(data)
        return MSG(**loaded)


def new_watcher(redis_cli: Redis, option: WatcherOptions):
    option.init_config()
    w = RedisWatcher(redis_cli)
    rds = w.redis_cli
    if rds.ping() is False:
        raise Exception('Redis server is not available.')
    w.sub_client = rds.client().pubsub()
    w.pub_client = rds.client()
    w.init_config(option)
    w.close = False
    w.subscribe_thread.start()
    w.subscribe_event.wait(timeout=5)
    return w


def new_publish_watcher(redis_cli: Redis, option: WatcherOptions) -> RedisWatcher:
    option.init_config()
    w = RedisWatcher(redis_cli)
    rds = w.redis_cli
    if rds.ping() is False:
        raise Exception('Redis server is not available.')
    w.pub_client = rds.client()
    w.init_config(option)
    w.close = False
    return w


def callback_function(event) -> None:
    logger.debug(f'update for remove filtered policy callback, event: {event}')


class CasbinEnforcer:
    def __init__(
        self, app: Optional[Flask] = None, adapter: Optional[Adapter] = None
    ) -> None:
        self.app: Optional[Flask] = app
        self._e: Optional[Enforcer] = None
        self._a: Optional[Adapter] = adapter
        self._watcher: Optional[RedisWatcher] = None

    def init_app(self, app: Flask) -> None:
        self.app = app
        assert self.app is not None
        model = self.app.config.get('CASBIN_MODEL_PATH')
        if model is None:
            raise ServiceConfigException(ExtensionMessage.CASBIN_MODEL_PATH_ERROR)

        self._e = Enforcer(model, self._a or self._default_adapter())
        if self.app.config.get('ENABLE_WATCHER'):
            from backend.extensions import redis
            options = WatcherOptions()
            options.optional_update_callback = self.update_callback
            w = new_watcher(redis.client, options)
            self._e.set_watcher(w)

    @property
    def e(self) -> Enforcer:
        return self._e

    def update_callback(self, message: str):
        logger.info(f'Policies has been changed: {message}')

    def _default_adapter(self) -> Adapter:
        return self._sqlalchemy_adapter

    @property
    def _sqlalchemy_adapter(self) -> Adapter:
        assert self.app is not None
        with self.app.app_context():
            return SQLAdapter(current_app.extensions['sqlalchemy'].db.engine)
