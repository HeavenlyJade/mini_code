import uuid
import datetime as dt
from typing import Dict, Any, List, Optional
from flask import current_app
from kit.service.base import CRUDService
from backend.mini_core.domain.order.order import ShopOrder
from backend.mini_core.repository.order.order_sqla import ShopOrderSQLARepository

__all__ = ['ShopOrderService']


class ShopOrderService(CRUDService[ShopOrder]):
    def __init__(self, repo: ShopOrderSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopOrderSQLARepository:
        return self._repo

    def get_order_list(self, args: dict) -> Dict[str, Any]:
        """获取订单列表"""
        # 处理时间范围查询
        if 'start_time' in args and 'end_time' in args:
            args['create_time'] = [args.pop('start_time'), args.pop('end_time')]

        if 'payment_start_time' in args and 'payment_end_time' in args:
            args['payment_time'] = [args.pop('payment_start_time'), args.pop('payment_end_time')]

        if 'ship_start_time' in args and 'ship_end_time' in args:
            args['ship_time'] = [args.pop('ship_start_time'), args.pop('ship_end_time')]

        # 处理金额范围查询
        if 'min_amount' in args and 'max_amount' in args:
            args['actual_amount'] = [args.pop('min_amount'), args.pop('max_amount')]
        data, total = self._repo.list(**args)
        return dict(data=data, code=200, total=total)

    def get_order_by_id(self, order_id: int) -> Dict[str, Any]:
        """通过ID获取订单"""
        data = self._repo.get_by_id(order_id)
        return dict(data=data, code=200)

    def get_order_by_order_no(self, order_no: str) -> Dict[str, Any]:
        """通过订单编号获取订单"""
        data = self._repo.get_by_order_no(order_no)
        return dict(data=data, code=200)

    def get_order_by_order_sn(self, order_sn: str) -> Dict[str, Any]:
        """通过订单号获取订单"""
        data = self._repo.get_by_order_sn(order_sn)
        return dict(data=data, code=200)

    def get_user_orders(self, user_id: int) -> Dict[str, Any]:
        """获取用户的订单"""
        data = self._repo.get_user_orders(user_id)
        return dict(data=data, code=200, total=len(data))

    def get_order_stats(self) -> Dict[str, Any]:
        """获取订单统计信息"""
        stats = self._repo.get_order_stats()
        return dict(data=stats, code=200)

    def get_monthly_sales(self) -> Dict[str, Any]:
        """获取月度销售统计"""
        data = self._repo.get_monthly_sales()
        return dict(data=data, code=200)

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建订单

        验证购物车数据和商品信息，创建订单记录
        """
        import json
        from decimal import Decimal
        import datetime as dt
        import uuid
        from backend.mini_core.repository import (shop_order_cart_sqla_repo, shop_product_sqla_repo)

        # 生成订单编号和订单号
        now = dt.datetime.now()
        order_no = f"ORD{now.strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"
        order_sn = f"SN{now.strftime('%Y%m%d')}{str(uuid.uuid4().int)[:8]}"

        # 解析用户信息
        user_detail = json.loads(order_data.get('userDetail', '{}'))
        user_id = user_detail.get('id')

        if not user_id:
            return dict(data=None, code=400, message="用户信息不完整")

        # 解析商品详情
        goods_detail = json.loads(order_data.get('goodsDetail', '[]'))
        if not goods_detail:
            return dict(data=None, code=400, message="商品信息不完整")

        # 验证购物车数据和商品信息
        cart_items = []
        product_amount = Decimal('0')
        product_count = 0

        for item in goods_detail:
            product_id = item.get('product_id')
            cart_id = item.get('cart_id')
            number = item.get('number', 0)
            price = item.get('price')

            # 1. 验证购物车项是否存在
            product = shop_product_sqla_repo.find(**{'id': product_id})
            # 2. 验证商品是否存在并检查价格
            if not product:
                return dict(data=None, code=400, message=f"商品不存在: {product_id}")
            # 验证价格是否一致（允许少量误差）
            if abs(Decimal(str(price)) - product.price) > Decimal('0.01'):
                return dict(data=None, code=400, message=f"商品价格不一致: {product.name}")
            # 验证库存是否足够
            if product.stock < number:
                return dict(data=None, code=400, message=f"商品库存不足: {product.name}，当前库存: {product.stock}")

            # 收集商品信息
            cart_items.append({
                'cart_id': cart_id,
                'product_id': product_id,
                'product_name': product.name,
                'product_img': product.images[0] if product.images else None,
                'price': product.price,
                'number': number,
                'subtotal': product.price * number
            })

            # 累计金额和数量
            product_amount += Decimal(str(price)) * Decimal(str(number))
            product_count += number

        # 解析收货地址
        address_info = json.loads(order_data.get('address', '{}'))

        # 设置订单基础信息
        order_data_to_save = {
            'order_no': order_no,
            'order_sn': order_sn,
            'user_id': user_id,
            'nickname': user_detail.get('nickname', ''),
            'phone': address_info.get('mobile', ''),
            'order_type': '普通订单',
            'order_source': '小程序',
            'status': '待支付',
            'payment_status': '待支付',
            'delivery_status': '未发货',
            'refund_status': '无退款',
            'product_count': product_count,
            'product_amount': product_amount,
            'actual_amount': product_amount,
            'discount_amount': order_data.get('benefit', Decimal('0')),
            'freight_amount': order_data.get('postage', Decimal('0')),
            'receiver_name': address_info.get('name', ''),
            'receiver_phone': address_info.get('mobile', ''),
            'province': address_info.get('pickerText', '').split('-')[0] if '-' in address_info.get('pickerText',
                                                                                                    '') else '',
            'city': address_info.get('pickerText', '').split('-')[1] if '-' in address_info.get('pickerText',
                                                                                                '') and len(
                address_info.get('pickerText', '').split('-')) > 1 else '',
            'district': address_info.get('pickerText', '').split('-')[2] if '-' in address_info.get('pickerText',
                                                                                                    '') and len(
                address_info.get('pickerText', '').split('-')) > 2 else '',
            'address': address_info.get('addressName', ''),
            'client_remark': order_data.get('memo', ''),
            'transaction_time': now
        }

        # 处理折扣金额
        discount_amount = order_data.get('benefit', Decimal('0'))
        if discount_amount:
            order_data_to_save['actual_amount'] = product_amount - discount_amount

        # 处理运费
        freight_amount = order_data.get('postage', Decimal('0'))
        if freight_amount:
            order_data_to_save['actual_amount'] = order_data_to_save['actual_amount'] + freight_amount

        # 创建订单，使用事务操作
        args = {
            "order_data_to_save": order_data_to_save,
            "cart_items": cart_items,
            "order_no": order_no
        }

        # 调用事务方法创建订单和相关数据
        return self._repo.order_create(args)
    def update_order_status(self, order_id: int, status: str) -> Dict[str, Any]:
        """更新订单状态"""
        order = self._repo.update_order_status(order_id, status)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        return dict(data=order, code=200)

    def update_payment_status(self, order_id: int, payment_status: str, payment_no: str = None, trade_no: str = None) -> \
    Dict[str, Any]:
        """更新支付状态"""
        order = self._repo.get_by_id(order_id)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        order.payment_status = payment_status
        if payment_status == '已支付':
            order.payment_time = dt.datetime.now()
            order.status = '已支付'

            # 更新支付信息
            if payment_no:
                order.payment_no = payment_no
            if trade_no:
                order.trade_no = trade_no

        self._repo.update(order_id, order)
        return dict(data=order, code=200)

    def update_delivery_status(self, order_id: int, delivery_status: str, express_company: str = None,
                               express_no: str = None, delivery_platform: str = None) -> Dict[str, Any]:
        """更新配送状态"""
        order = self._repo.get_by_id(order_id)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        order.delivery_status = delivery_status

        if delivery_status == '已发货':
            order.ship_time = dt.datetime.now()
            order.status = '已发货'

            # 更新物流信息
            if express_company:
                order.express_company = express_company
            if express_no:
                order.express_no = express_no
            if delivery_platform:
                order.delivery_platform = delivery_platform

        elif delivery_status == '已签收':
            order.confirm_time = dt.datetime.now()
            order.status = '已完成'

        self._repo.update(order_id, order)
        return dict(data=order, code=200)

    def update_refund_status(self, order_id: int, refund_status: str) -> Dict[str, Any]:
        """更新退款状态"""
        order = self._repo.update_refund_status(order_id, refund_status)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        return dict(data=order, code=200)

    def close_order(self, order_id: int) -> Dict[str, Any]:
        """关闭订单"""
        order = self._repo.close_order(order_id)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        return dict(data=order, code=200)

    def confirm_receipt(self, order_id: int) -> Dict[str, Any]:
        """确认收货"""
        order = self._repo.get_by_id(order_id)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        if order.delivery_status != '已发货':
            return dict(data=None, code=400, message="订单未发货，无法确认收货")

        order.delivery_status = '已签收'
        order.status = '已完成'
        order.confirm_time = dt.datetime.now()

        self._repo.update(order_id, order)
        return dict(data=order, code=200)

    def cancel_order(self, order_id: int) -> Dict[str, Any]:
        """取消订单"""
        order = self._repo.get_by_id(order_id)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        if order.status not in ['待支付', '已支付', '待发货']:
            return dict(data=None, code=400, message="当前订单状态不允许取消")

        order.status = '已取消'
        order.close_time = dt.datetime.now()

        self._repo.update(order_id, order)
        return dict(data=order, code=200)
