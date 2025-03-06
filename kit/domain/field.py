from abc import abstractmethod
from enum import Enum, unique

__all__ = ['ExtendedEnum', 'ExtendedIntEnum']


@unique
class ExtendedEnum(Enum):
    __doc__ = '枚举类型'

    @classmethod
    @abstractmethod
    def comparison_map(cls) -> dict:
        ...

    @classmethod
    def desc(cls) -> str:
        return (
            f'{cls.__doc__}: '
            f'{", ".join(value + "--" + str(key) for key, value in cls.comparison_map().items())}'
        )

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass


class ExtendedIntEnum(int, ExtendedEnum):
    @classmethod
    @abstractmethod
    def comparison_map(cls) -> dict:
        ...
