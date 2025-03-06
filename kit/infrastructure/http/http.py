from abc import abstractmethod
from typing import Any

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout

from kit.exceptions import ServiceBadRequest
from kit.message import RequestMessage


class HTTPClient:
    @property
    @abstractmethod
    def endpoint_url(self) -> str:
        ...

    def retry(self):
        ...

    def fetch_req(self, url: str, params: Any = None, **kwargs) -> Any:
        resp: requests.Response = self._request('get', url, params=params, **kwargs)
        items = resp.json()
        return items

    def post_req(self, url: str, data: Any = None, json: dict = None, **kwargs):
        resp: requests.Response = self._request(
            'post', url, data=data, json=json, **kwargs
        )
        items = resp.json()
        return items

    def put_req(self, url: str, data: Any = None, **kwargs):
        resp: requests.Response = self._request('put', url, data=data, **kwargs)
        items = resp.json()
        return items

    def patch_req(self, url: str, data: Any = None, **kwargs):
        resp: requests.Response = self._request('patch', url, data=data, **kwargs)
        items = resp.json()
        return items

    def delete_req(self, url: str, **kwargs):
        return self._request('delete', url, **kwargs)

    @classmethod
    def _request(cls, method: str, url: str, **kwargs):
        try:
            resp: requests.Response = requests.request(method=method, url=url, **kwargs)
        except ConnectionError:
            raise ServiceBadRequest(RequestMessage.CONNECT_ERROR)
        except (ConnectTimeout, ReadTimeout):
            raise ServiceBadRequest(RequestMessage.CONNECT_TIMEOUT_ERROR)
        except Exception as e:
            raise ServiceBadRequest(f'请求出错：{str(e)}')
        if not resp.ok:
            if resp.status_code == 404:
                return resp
            elif 'message' in resp.json():
                message = resp.json()['message']
            else:
                message = RequestMessage.CONNECT_ERROR
            raise ServiceBadRequest(message)
        return resp
