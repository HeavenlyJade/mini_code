from typing import Optional

import socketio
from flask import Flask
from socketio import BaseManager

from kit.exceptions import ServiceConfigException
from kit.message import ExtensionMessage

__all__ = ['SocketIOApp']


class SocketIOApp:
    def __init__(self, app: Flask = None):
        self.app: Optional[Flask] = app
        self.sio_server: Optional[socketio.Server] = None
        self.external_sio: Optional[BaseManager] = None

        if app:
            self.init_app(app)

    def init_app(
        self,
        app: Flask,
        sio_server: Optional[socketio.Server] = None,
    ):
        self.app = app
        self.sio_server = sio_server or self._default_sio_server()
        self.external_sio = self._default_external_sio()

    def _default_sio_server(self):
        return self._redis_sio_server

    @property
    def _redis_sio_server(self) -> socketio.Server:
        url = self.app.config.get('REDIS_URL')
        if not url:
            raise ServiceConfigException(ExtensionMessage.REDIS_CONNECT_ERROR)
        options = dict()
        if password := self.app.config.get('REDIS_PASSWORD'):
            options['password'] = password
        mgr = socketio.RedisManager(url, redis_options=options)
        sio = socketio.Server(
            client_manager=mgr,
            logger=True,
            engineio_logger=True,
            cors_allowed_origins='*',
            async_mode='eventlet',
        )
        return sio

    def _default_external_sio(self) -> BaseManager:
        url = self.app.config.get('REDIS_URL')
        if not url:
            raise ServiceConfigException(ExtensionMessage.REDIS_CONNECT_ERROR)
        options = dict()
        if password := self.app.config.get('REDIS_PASSWORD'):
            options['password'] = password
        sio = socketio.RedisManager(
            url, write_only=True, logger=True, redis_options=options
        )
        return sio
