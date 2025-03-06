from typing import Any, Dict, List, Optional, Sequence, Tuple

from backend.business.domain.product import Product
from backend.business.repository.product.base import ProductRepository
from kit.repository.generic import T


class ProductMockRepository(ProductRepository):
    def list(self, **kwargs) -> Tuple[List[Product], int]:
        mock_qty = 100
        products = list()
        for i in range(1, mock_qty):
            product = Product()
            product.id = i
            product.product_name = f'product-{i}'
            products.append(product)
        return products, mock_qty

    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    def create(self, entity: T, commit: bool = True) -> T:
        pass

    def update(self, entity_id: int, entity: T, commit: bool = True) -> Optional[T]:
        pass

    def delete(self):
        pass

    def delete_by(self, conditions: Dict[str, Any], commit: bool = True):
        pass

    def create_many(self, entities: List[T], commit: bool = True) -> None:
        pass

    def find(self, **kwargs) -> Optional[T]:
        pass

    def find_by_ids(self, ids: Sequence[int]) -> List[T]:
        pass

    def find_all(self, **kwargs) -> List[T]:
        pass

    def get_all(self, **kwargs) -> List[T]:
        ...

    def commit(self) -> None:
        ...

