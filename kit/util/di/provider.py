from abc import ABC, abstractmethod
from typing import Callable, Optional

__all__ = ['Factory', 'Selector']


class Provider(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...


class Factory(Provider):
    def __init__(self, provides: Callable, *args, **kwargs) -> None:
        self.provides: Callable = provides
        self.args: tuple = args
        self.kwargs: dict = kwargs

    def __call__(self, *args, **kwargs):
        return self.provides(*self.args, **self.kwargs)


class Selector:
    def __init__(self, select_tag: str, config_map: dict, /, **providers: Provider):
        self.select_tag: str = select_tag
        self.config_map: dict = config_map
        self.providers: dict = providers

    def __call__(self, *args, **kwargs) -> Provider:
        select_value: Optional[str] = self.config_map.get(self.select_tag)
        if not select_value or select_value not in self.providers:
            raise NotImplementedError

        return self.providers[select_value]()
