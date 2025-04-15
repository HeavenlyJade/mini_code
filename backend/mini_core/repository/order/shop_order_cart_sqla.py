import datetime as dt
from typing import Type, Tuple, List, Dict, Any

from sqlalchemy import Column, String, Table, Integer, DateTime, BigInteger, func

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.shop_order_cart import ShopOrderCart
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['ShopOrderCartSQLARepository']

# 购物车表
shop_order_cart_table = Table(
    'shop_order_cart',
    mapper_registry.metadata,
    id_column(),
    Column('user_id', String(64), nullable=False, index=True, comment='用户ID'),
    Column('open_id', String(255), comment='微信openID'),
    Column('sku_id', Integer, comment='商品SKU ID'),
    Column('product_count', Integer, nullable=False, comment='商品数量'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
)

# 映射关系
mapper_registry.map_imperatively(ShopOrderCart, shop_order_cart_table)


class ShopOrderCartSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopOrderCart]:
        return ShopOrderCart

    @property
    def query_params(self) -> Tuple:
        return 'user_id', 'open_id', 'sku_id'

    def get_cart_items_with_products(self, user_id: str) -> List[Dict[str, Any]]:
        """
        获取用户购物车商品及其详细信息（联表查询）

        Args:
            user_id: 用户ID

        Returns:
            购物车商品及其详细信息列表
        """
        # 使用SQL原生查询进行联表操作
        import json
        sql = """
        SELECT
            c.id as cart_id,
            c.user_id,
            c.open_id,
            c.sku_id,
            c.product_count,
            c.create_time as cart_create_time,
            c.update_time as cart_update_time,
            p.id as product_id,
            p.name as product_name,
            p.price,
            p.market_price,
            p.stock,
            p.images,
            p.spec_combinations as product_spec,
            p.status as product_status
        FROM
            shop_order_cart c
        LEFT JOIN
            shop_product p ON c.sku_id = p.id
        WHERE
            c.user_id = :user_id
        ORDER BY
            c.update_time DESC
        """

        result = self.session.execute(sql, {'user_id': user_id}).fetchall()

        # 将结果转换为字典列表
        cart_items = []
        for row in result:
            # 转换为字典
            row_dict = dict(row)

            # 处理images字段（假设是JSON格式字符串）
            if 'images' in row_dict and row_dict['images']:
                try:
                    row_dict['images'] = json.loads(row_dict['images'])
                except:
                    # 如果解析失败，保持原样
                    pass

            # 计算小计金额
            if 'price' in row_dict and 'product_count' in row_dict:
                row_dict['subtotal'] = float(row_dict['price']) * row_dict['product_count']

            cart_items.append(row_dict)

        return cart_items
    def get_user_cart_items(self, user_id: str) -> List[ShopOrderCart]:
        """获取用户的所有购物车商品"""
        return self.find_all(user_id=user_id)

    def get_user_cart_by_openid(self, open_id: str) -> List[ShopOrderCart]:
        """通过微信openID获取用户的购物车"""
        return self.find_all(open_id=open_id)

    def get_cart_item(self, user_id: str, sku_id: int) -> ShopOrderCart:
        """获取用户购物车中的特定商品"""
        return self.find(user_id=user_id, sku_id=sku_id)

    def update_cart_item_quantity(self, cart_id: int, quantity: int) -> ShopOrderCart:
        """更新购物车商品数量"""
        cart_item = self.get_by_id(cart_id)
        if cart_item:
            cart_item.product_count = quantity
            self.session.commit()
        return cart_item

    def delete_by_user_and_sku(self, user_id: str, sku_id: int) -> None:
        """删除用户购物车中的特定商品"""
        self.delete_by({'user_id': user_id, 'sku_id': sku_id})

    def clear_user_cart(self, user_id: str) -> None:
        """清空用户购物车"""
        self.delete_by({'user_id': user_id})

    def get_cart_count(self, user_id: str) -> int:
        """获取用户购物车商品总数"""
        result = self.session.query(func.sum(ShopOrderCart.product_count))\
            .filter(ShopOrderCart.user_id == user_id)\
            .scalar()
        return result or 0
