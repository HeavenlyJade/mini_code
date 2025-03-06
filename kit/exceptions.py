"""Custom exceptions."""
from typing import Optional


class ServiceException(Exception):
    status_code = 500

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        payload: Optional[int] = None,
    ):
        super().__init__()
        self.message: str = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def __iter__(self):
        for k in ['message']:
            yield k, getattr(self, k)


class ServiceConfigException(ServiceException):
    pass


class ServiceClientException(ServiceException):
    ...


class ServiceBadRequest(ServiceClientException):
    status_code = 400


class ServiceNotFound(ServiceClientException):
    status_code = 404
