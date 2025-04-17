from decimal import Decimal
from typing import List, Dict, Any, Optional
from flask_jwt_extended import get_current_user
from flask import g

from backend.mini_core.domain.order.shop_order_cart import ShopOrderCart
from backend.mini_core.repository.order.shop_order_cart_sqla import ShopOrderCartSQLARepository
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService

__all__ = ['ShopOrderCartService']


class ShopOrderCartService(CRUDService[ShopOrderCart]):
    def __init__(self, repo: ShopOrderCartSQLARepository):
        super().__init__(repo)
        self._repo = repo
        self._product_repo = None  # 将在使用时初始化，避免循环引用

    @property
    def repo(self) -> ShopOrderCartSQLARepository:
        return self._repo

    @property
    def product_repo(self):
        """获取商品仓储实例"""
        if self._product_repo is None:
            # 延迟导入，避免循环引用
            from backend.mini_core.repository import shop_product_sqla_repo
            self._product_repo = shop_product_sqla_repo
        return self._product_repo

    def get_user_cart(self,) -> Dict[str, Any]:
        """获取用户购物车"""
        # 使用联表查询方法获取购物车和商品信息
        user = get_current_user()
        user_id = user.id
        cart_items_with_product_data = self._repo.get_cart_items_with_products(str(user_id))

        # 初始化统计数据
        total_price = Decimal('0')
        total_count = 0
        cart_items_with_product = []

        # 处理查询结果，重新格式化为前端所需的格式
        for item in cart_items_with_product_data:
            # 只处理有效商品（存在且有库存）
            if not item or item.get('product_id') is None:
                continue

            # 计算商品小计金额并累计总价和总数量
            product_count = item.get('product_count', 0)
            price = Decimal(str(item.get('price', 0)))
            item_price = price * product_count
            total_price += item_price
            total_count += product_count
            item["item_price"] = item_price
            cart_items_with_product.append(item)
        # 返回与原方法一致的响应格式
        return {
            'data': cart_items_with_product,
            'total': len(cart_items_with_product),
            'total_count': total_count,
            'total_price': float(total_price),
            'code': 200
        }
    def add_to_cart(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """添加商品到购物车"""
        # 获取当前用户对象
        user = get_current_user()
        print("user",user)
        open_id = user.openid
        user_id = user.id
        quantity = item_data.get('product_count',)
        sku_id = item_data.get('sku_id')
        # 检查商品是否存在
        product_info = self._get_product_info(sku_id)
        if not product_info:
            return {'code': 404, 'message': '商品不存在'}

        # 检查库存
        if product_info.get('stock', 0) < quantity:
            return {'code': 400, 'message': '商品库存不足'}

        # 检查是否已在购物车
        existing_item = self._repo.get_cart_item(user_id, sku_id)

        if existing_item:
            # 更新数量
            new_quantity = existing_item.product_count + quantity
            if product_info.get('stock', 0) < new_quantity:
                return {'code': 400, 'message': '商品库存不足'}
            existing_item.product_count = new_quantity
            self._set_updater(existing_item)
            result = self._repo.update(existing_item.id, existing_item)
        else:
            # 创建新购物车项
            cart_item = ShopOrderCart(
                user_id=user_id,
                open_id=open_id,
                sku_id=sku_id,
                product_count=quantity
            )
            self._set_updater(cart_item)
            result = self._repo.create(cart_item)

        return {'data': result, 'code': 200, 'message': '商品已添加到购物车'}

    def update_cart_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新购物车商品数量"""
        cart_id = item_data.get('id')
        quantity = item_data.get('product_count')

        cart_item = self._repo.get_by_id(cart_id)
        if not cart_item:
            return {'code': 404, 'message': '购物车项不存在'}

        # 检查商品是否存在
        product_info = self._get_product_info(cart_item.sku_id)
        if not product_info:
            return {'code': 404, 'message': '商品不存在'}

        # 检查库存
        if product_info.get('stock', 0) < quantity:
            return {'code': 400, 'message': '商品库存不足'}

        # 更新数量
        cart_item.product_count = quantity
        self._set_updater(cart_item)
        result = self._repo.update(cart_id, cart_item)

        return {'data': result, 'code': 200, 'message': '购物车已更新'}

    def delete_cart_item(self,  sku_id: int) -> Dict[str, Any]:
        """删除购物车商品"""
        user = get_current_user()
        user_id = str(user.id)
        self._repo.delete_by_user_and_sku(user_id, sku_id)
        return {'code': 200, 'message': '商品已从购物车删除'}

    def clear_cart(self, user_id: str) -> Dict[str, Any]:
        """清空购物车"""
        self._repo.clear_user_cart(user_id)
        return {'code': 200, 'message': '购物车已清空'}

    def get_cart_count(self, user_id: str) -> Dict[str, Any]:
        """获取购物车商品总数"""
        count = self._repo.get_cart_count(user_id)
        return {'data': {'count': count}, 'code': 200}

    def _set_updater(self, entity: ShopOrderCart) -> None:
        """设置更新者"""
        current_user = get_current_user()
        if hasattr(current_user, 'username'):
            entity.updater = current_user.username
        elif hasattr(g, 'user_id'):
            entity.updater = g.user_id

    def _get_product_info(self, sku_id: int) -> Optional[Dict[str, Any]]:
        """获取商品信息"""
        # 这里需要根据实际的商品仓储接口调整
        try:
            # 查询商品信息
            product = self.product_repo.find(id=sku_id)
            if product:
                return {
                    'id': product.id,
                    'name': product.name,
                    'images': product.images,
                    'price': product.price,
                    'market_price': product.market_price,
                    'stock': product.stock,
                    'product_spec': product.specifications
                }
        except Exception as e:
            # 记录异常但不中断流程
            print(f"Error fetching product info for sku_id {sku_id}: {str(e)}")

        return None
