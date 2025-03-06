from backend.business.domain.product import Product
from kit.service.base import CRUDService

__all__ = ['ProductService']


class ProductService(CRUDService[Product]):
    ...
