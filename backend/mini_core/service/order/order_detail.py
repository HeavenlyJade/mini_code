from decimal import Decimal
from typing import List, Dict, Any

from backend.mini_core.domain.order.order_detail import OrderDetail
from backend.mini_core.repository.order.order_detail_sql import OrderDetailSQLARepository
from kit.service.base import CRUDService

__all__ = ['OrderDetailService']


class OrderDetailService(CRUDService[OrderDetail]):
    def __init__(self, repo: OrderDetailSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> OrderDetailSQLARepository:
        return self._repo

    def get_order_detail_list(self, **kwargs):
        print(kwargs)
        data, total = self._repo.list(**kwargs)

        return dict(order_details=data, total=total, code=200)

    def get_order_details(self, order_no: str) -> Dict[str, Any]:
        """获取指定订单的所有订单详情"""
        details = self._repo.get_order_details(order_no)
        re_data = dict(data=details, code=200)
        re_data.update(details)
        return re_data

    def get_gift_details(self, order_no: str) -> Dict[str, Any]:
        """获取指定订单的所有赠品详情"""
        details = self._repo.get_gift_details(order_no)
        return dict(data=details, code=200, )

    def create_order_detail(self, detail: Dict[str, Any]) -> Dict[str, Any]:
        """创建订单详情"""
        # 计算total_price (如果未提供)
        if 'total_price' not in detail or not detail['total_price']:
            detail['total_price'] = Decimal(str(detail['actual_price'])) * Decimal(str(detail['num']))

        # 如果未提供unit_price，则使用price
        if 'unit_price' not in detail or not detail['unit_price']:
            detail['unit_price'] = detail['price']

        # 如果未提供quantity，则使用num
        if 'quantity' not in detail or not detail['quantity']:
            detail['quantity'] = detail['num']

        result = self.create(OrderDetail(**detail))
        return dict(data=result, code=200)

    def batch_create_details(self, details: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量创建订单详情"""
        detail_objects = []

        for detail in details:
            # 计算total_price (如果未提供)
            if 'total_price' not in detail or not detail['total_price']:
                detail['total_price'] = Decimal(str(detail['actual_price'])) * Decimal(str(detail['num']))

            # 如果未提供unit_price，则使用price
            if 'unit_price' not in detail or not detail['unit_price']:
                detail['unit_price'] = detail['price']

            # 如果未提供quantity，则使用num
            if 'quantity' not in detail or not detail['quantity']:
                detail['quantity'] = detail['num']

            detail_objects.append(OrderDetail(**detail))

        self._repo.batch_create_details(detail_objects)
        return dict(code=200, message=f"成功创建{len(detail_objects)}个订单详情")

    def get_product_orders(self, product_id: int) -> Dict[str, Any]:
        """获取指定商品的所有订单详情"""
        details = self._repo.find_all(product_id=product_id)
        return dict(data=details, code=200, total=len(details))

    def update_detail(self, detail_id: int, detail_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新订单详情"""
        result = self.update(detail_id, OrderDetail(**detail_data))
        return dict(data=result, code=200)

    def delete_detail(self, detail_id: int) -> Dict[str, Any]:
        """删除订单详情"""
        self.delete(detail_id)
        return dict(code=200, message="订单详情删除成功")

    def get_order_amount(self, order_no: str) -> Dict[str, Any]:
        """计算订单总金额"""
        details = self._repo.get_order_details(order_no)

        total_original_amount = sum(detail.price * detail.num for detail in details)
        total_actual_amount = sum(detail.actual_price * detail.num for detail in details)
        total_items = sum(detail.num for detail in details)

        return dict(
            code=200,
            data={
                "order_no": order_no,
                "original_amount": float(total_original_amount),
                "actual_amount": float(total_actual_amount),
                "total_items": total_items,
                "discount_amount": float(total_original_amount - total_actual_amount)
            }
        )
