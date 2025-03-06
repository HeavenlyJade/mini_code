from backend.business.repository.product import product_mock_repo


from .enums import EnumService
from .product import ProductService

enum_service = EnumService()
product_service = ProductService(product_mock_repo)
