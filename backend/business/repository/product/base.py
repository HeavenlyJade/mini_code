from abc import ABCMeta

from backend.business.domain.product import Product
from kit.repository.generic import GenericRepository

__all__ = ['ProductRepository']


class ProductRepository(GenericRepository[Product], metaclass=ABCMeta):
    ...
