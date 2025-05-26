import uuid
import datetime as dt
from typing import Dict, Any, List, Optional
from flask import current_app
from flask_jwt_extended import get_current_user

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

    def get_order_detail_msg(self, args: dict):
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        return self._repo.get_order_msg(user_id=user_id, args=args)

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
        if not "ordering" in args:
            args['ordering'] = ['-update_time']
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
        from backend.mini_core.repository import  shop_product_sqla_repo

        # 生成订单编号和订单号
        now = dt.datetime.now()
        order_no = f"ORD{now.strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"
        order_sn = f"SN{now.strftime('%Y%m%d')}{str(uuid.uuid4().int)[:8]}"
        amount = Decimal(order_data['amount'])
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
        bac_amount = 0
        product_name=""
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
            bac_amount += product.price * number
            product_name += " \n"+product.name
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
        if bac_amount != amount:
            return dict(data=None, code=400, message=f"价格订单和: 商城订单不一致")
        # 设置订单基础信息
        order_data_to_save = {
            'order_no': order_no,
            'order_sn': order_sn,
            "product_name":product_name,
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

    def update_order_status(self, order_no: str, status: str) -> Dict[str, Any]:
        """更新订单状态"""
        order = self._repo.update_order_status(order_no, status)
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

    def update_refund_status(self, order_no: str, refund_status: str) -> Dict[str, Any]:
        """更新退款状态"""
        order = self._repo.update_order_status(order_no, refund_status)
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

    def change_order_to_paid(self, order_id: int) -> Dict[str, Any]:
        """将订单从待支付状态变更为已支付状态"""
        from backend.mini_core.service.shop_app.wx_server_new import WechatPayService
        order = self._repo.get_by_id(order_id)
        args_dict = dict(out_trade_no=order.order_no)
        result = WechatPayService.query_order(args_dict)
        data = result.get("data",{})
        transaction_id = data.get('transaction_id')
        trade_state_desc = data.get('trade_state_desc')
        trade_state = data.get('trade_state')
        trade_type = data.get("trade_type")
        current_user = get_current_user()
        current_user_id = current_user.id
        if not transaction_id and trade_state!="SUCCESS":
            return dict(data=None, code=400, message="微信查询的订单不是支付成功，请联系客服")

        if order and str(order.user_id) == str(current_user_id):
            order_user_id = order.user_id
            # if order.payment_status == '待支付':
            order.payment_status = '已支付'
            order.status = '待发货'
            order.payment_no= transaction_id
            order.pay_method =trade_type
            order.payment_time = dt.datetime.now()
            self._repo.session.commit()

        if not order:
            return dict(data=None, code=400, message="订单不存在或当前状态不允许变更为已支付")

        return dict(data=order, code=200, message="订单已成功变更为已支付状态")

    def update_shipping_info(self, order_no: str, shipping_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新订单的物流信息，同时在物流表中创建或更新对应记录

        参数:
            order_no: 订单编号
            shipping_data: 包含物流信息的字典，可包含以下字段:
                - express_company: 快递公司
                - express_no: 快递单号
                - delivery_platform: 配送平台
                - remark: 备注

        返回:
            Dict[str, Any]: 包含更新结果的字典
        """

        # 同步更新物流表中的记录
        from backend.mini_core.service import shop_order_logistics_service
        from backend.mini_core.domain.order.shop_order_logistics import ShopOrderLogistics
        import json
        order:ShopOrder = self._repo.find(order_no=order_no)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        # 获取当前用户和时间信息
        current_user = get_current_user()
        operator = current_user.username if hasattr(current_user, 'username') else 'system'
        current_time = dt.datetime.now()
        express_company = shipping_data.get('express_company')
        express_no = shipping_data.get('express_no')
        delivery_platform = shipping_data.get('delivery_platform')
        remark = shipping_data.get('remark')
        # 更新物流信息字段
        if express_company:
            order.express_company = express_company
        if express_no:
            order.express_no = shipping_data['express_no']
        if delivery_platform:
            order.delivery_platform = shipping_data['delivery_platform']
        if remark:
            order.remark = shipping_data['remark']

        # 更新订单状态
        order.status = '已发货'
        order.delivery_status = '已发货'
        order.ship_time = current_time
        order_id = order.id
        order.updater = operator



        # 获取收件人信息
        receiver_info = {
            "name": order.receiver_name,
            "phone": order.receiver_phone,
            "province": order.province,
            "city": order.city,
        }

        # 获取现有物流记录或创建新记录
        logistics_data = shop_order_logistics_service.get_logistics_by_order_no(order_no)

        if logistics_data and logistics_data.get('data'):
            # 更新现有物流记录
            logistics = logistics_data.get('data')
            logistics_id = logistics.id
            # 准备更新的物流数据
            logistics_update = {
                'logistics_company': order.express_company,
                'logistics_no': order.express_no,
                'current_status': '已发货',
                'shipping_time': current_time,
                'estimate_time': current_time + dt.timedelta(days=3),  # 预计3天送达
                'receiver_info': receiver_info
            }

            # 添加物流轨迹记录
            if logistics.logistics_route:
                try:
                    route = json.loads(logistics.logistics_route)
                except:
                    route = []
            else:
                route = []

            # 添加新的轨迹节点
            route.append({
                'time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': '已发货',
                'location': shipping_data.get('current_location', ''),
                'remark': f'商家已发货: {order.express_company} {order.express_no}'
            })

            logistics_update['logistics_route'] = json.dumps(route)

            # 更新物流记录
            shop_order_logistics_service.update_logistics(logistics_id, logistics_update)
        else:
            # 创建新的物流记录
            new_logistics = ShopOrderLogistics(
                order_no=order_no,
                logistics_no=order.express_no,
                logistics_company=order.express_company,
                courier_number=shipping_data.get('courier_number',),
                courier_phone=shipping_data.get('courier_phone',),
                receiver_info=receiver_info,
                shipping_time=current_time,
                estimate_time=current_time + dt.timedelta(days=3),  # 预计3天送达
                current_status='已发货',
                current_location=shipping_data.get('current_location'),
                start_date=current_time,
                remark=shipping_data.get('remark',),
                logistics_route={}

            )
            shop_order_logistics_service.create(new_logistics)
        result = self._repo.update(order_id, order)
        from backend.mini_core.service import order_log_service
        log_desc = f"更新物流信息: {order.express_company or ''} {order.express_no or ''}"
        if 'delivery_platform' in shipping_data and shipping_data['delivery_platform']:
            log_desc += f"，配送平台: {shipping_data['delivery_platform']}"
        order_log_service.create_log({
            'order_no': order.order_no,
            'operation_type': '物流信息更新',
            'operation_desc': log_desc,
            'operator': operator,
        })
        return dict(data=result, code=200, message="物流信息更新成功，物流跟踪已建立")
