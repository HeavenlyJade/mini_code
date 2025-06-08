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
        user = get_current_user()
        user_id = str(user.user_id)
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
        from backend.mini_core.service import member_level_config_service

        # 生成订单编号和订单号
        now = dt.datetime.now()
        order_no = f"ORD{now.strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}"
        order_sn = f"SN{now.strftime('%Y%m%d')}{str(uuid.uuid4().int)[:8]}"
        final_amount = Decimal(order_data['final_amount'])
        points_used = order_data.get("points_used",0)
        points_deduct_amount = order_data.get("points_deduct_amount",0)
        # 解析用户信息
        user_detail = json.loads(order_data.get('userDetail', '{}'))
        user = get_current_user()
        user_int_id = user.id
        user_id = str(user.user_id)
        user_points = user.points
        member_level = user.member_level
        member_level_config = member_level_config_service.find_level_data({"level_code": member_level})
        remaining_points = user_points - points_used
        if remaining_points< 0:
            return dict(data=None, code=400, message="实际积分数量不足")

        if not member_level_config:
            return dict(data=None, code=400, message="没有会员的等级信息")
        discount_rate =member_level_config.discount_rate
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

        discount_bac_amount = bac_amount * (discount_rate / 100)  # 打折后的价格
        discount_amount = bac_amount-discount_bac_amount   # 折扣后的价格
        dis_bac_amount = discount_bac_amount - points_used  # 折扣价格前去使用的积分
        if dis_bac_amount != final_amount:
            return dict(data=None, code=400, message=f"实际订单价格不一致")
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
            'actual_amount': final_amount,
            'discount_amount': discount_amount,
            'point_amount':points_used,
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

        user_data = dict(user_int_id=user_int_id,remaining_points=remaining_points,points_used=points_used)
        # 创建订单，使用事务操作
        args = {
            "order_data_to_save": order_data_to_save,
            "cart_items": cart_items,
            "order_no": order_no,
            "user_data":user_data
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

    def update_refund_status(self, order_no: str, refund_status: str) -> Dict[str, Any]:
        """更新退款状态"""
        order = self._repo.update_order_status(order_no, refund_status)
        if not order:
            return dict(data=None, code=404, message="订单不存在")
        refund_points_result = self.refund_order_points({}, order_no,"订单退款")

        return dict(data=order, code=200)

    def close_order(self, order_id: int) -> Dict[str, Any]:
        """关闭订单"""
        order = self._repo.close_order(order_id)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        return dict(data=order, code=200)

    def wx_confirm_receipt(self, order_no: str) -> Dict[str, Any]:
        """确认收货"""
        from backend.mini_core.service import shop_user_service
        from backend.mini_core.utils.redis_utils.log_queue import LogQueue

        current_user = get_current_user()
        current_user_id = current_user.user_id
        order: ShopOrder = self._repo.find(order_no=order_no)
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        if order.delivery_status != '已发货':
            return dict(data=None, code=400, message="订单未发货，无法确认收货")
        order_user_id = order.user_id
        if order_user_id != current_user_id:
            return dict(data=None, code=400, message="非当前用户不可修改订单")

        operator = current_user.username
        user = shop_user_service.find(user_id=order.user_id)
        original_points = user.points or 0
        actual_amount = order.actual_amount
        points_reward = float(actual_amount)
        new_points = original_points + points_reward

        # 准备更新数据
        order_update_data = {
            'delivery_status': '已签收',
            'status': '已完成',
            'confirm_time': dt.datetime.now(),
            'updater': operator
        }

        user_update_data = {
            'points': new_points
        }

        # 调用 repository 方法执行数据库操作
        result = self._repo.confirm_receipt_with_points(
            order_no, order_update_data, user_update_data
        )

        # 如果数据库操作成功，记录日志
        if result.get('code') == 200:
            LogQueue.add_order_log(
                order_no=order_no,
                operation_type='确认收货',
                operation_desc=f'确认收货完成，获得积分奖励 {points_reward} 分',
                operator=operator,
                old_value={
                    'order_status': order.status,
                    'delivery_status': order.delivery_status,
                    'user_points': original_points
                },
                new_value={
                    'order_status': '已完成',
                    'delivery_status': '已签收',
                    'user_points': new_points
                },
                remark=f'支付金额：{actual_amount}元，获得积分：{points_reward}分'
            )

        return dict(data=order_update_data, code=200)

    def cancel_order(self, args: dict) -> Dict[str, Any]:
        """取消订单"""
        order_no = args['order_no']
        order = self._repo.find(**{"order_no":order_no})
        if not order:
            return dict(data=None, code=404, message="订单不存在")

        if order.status not in ['待支付']:
            return dict(data=None, code=400, message="当前订单状态不允许取消")

        order.status = '已取消'
        order.close_time = dt.datetime.now()
        order_id = order.id
        self.refund_order_points(order, order_no, "用户主动取消订单")
        self._repo.update(order_id, order)
        return dict(data=order, code=200)

    def change_order_to_paid(self, order_id: int) -> Dict[str, Any]:
        """将订单从待支付状态变更为已支付状态"""
        from backend.mini_core.service.shop_app.wx_server_new import WechatPayService
        from backend.mini_core.service import  distribution_income_service
        order = self._repo.get_by_id(order_id)
        args_dict = dict(out_trade_no=order.order_no)
        result = WechatPayService.query_order(args_dict)
        data = result.get("data",{})
        transaction_id = data.get('transaction_id')
        trade_state_desc = data.get('trade_state_desc')
        trade_state = data.get('trade_state')
        trade_type = data.get("trade_type")
        current_user = get_current_user()
        current_user_id = current_user.user_id
        if not transaction_id and trade_state!="SUCCESS":
            return dict(data=None, code=400, message="微信查询的订单不是支付成功，请联系客服")
        if not order or order=="待支付":
            return dict(data=None, code=400, message="订单不存在或当前不是待支付")
        if str(order.user_id) != str(current_user_id):
            return dict(data=None, code=400, message="非当前用户不可变更订单")

        order.payment_status = '已支付'
        order.status = '待发货'
        order.payment_no= transaction_id
        order.pay_method =trade_type
        order.payment_time = dt.datetime.now()
        data = self.create_distribution_income(order)
        self.repo.session.commit()
        print("data",data)
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

    def refund_order_points(self,order_obj, order_no: str, reason: str = "订单取消/退款") -> Dict[str, Any]:
        """
        退还订单使用的积分给用户

        参数:
            order_no: 订单编号
            reason: 退款原因

        返回:
            Dict[str, Any]: 包含退款结果的字典
        """
        from backend.mini_core.service import shop_user_service
        from backend.mini_core.utils.redis_utils.log_queue import LogQueue
        # 获取订单信息
        if order_obj:
            order =order_obj
        else:
            order = self._repo.find(order_no=order_no)
            if not order:
                return dict(data=None, code=404, message="订单不存在")

        # 检查订单是否使用了积分
        points_used = order.point_amount if order.point_amount else 0
        if points_used <= 0:
            return dict(data=None, code=400, message="该订单未使用积分，无需退还")
        # 检查订单状态是否允许退款
        if order.status not in ['已取消', '已退款', '退款中']:
            return dict(data=None, code=400, message="订单状态不允许积分退款")
        user = shop_user_service.find(user_id=order.user_id)
        if not user:
            return dict(data=None, code=404, message="用户不存在")
        # 计算退还后的积分
        original_points = user.points or 0
        refund_points = int(points_used)
        new_points = original_points + refund_points
        # 更新用户积分
        user.points = new_points
        print(refund_points, original_points,new_points)

        shop_user_service.repo.update(user.id, user)
        # 记录积分退款日志
        current_user = get_current_user()
        operator = current_user.username if hasattr(current_user, 'username') else 'system'
        # 添加订单日志]
        operation_desc = f'订单取消/退款，退还积分 {refund_points} 分'
        LogQueue.add_order_log(
            order_no=order_no,
            operation_type='积分退还',
            operation_desc=f'订单取消/退款，退还积分 {refund_points} 分',
            operator=operator,
            old_value={'user_points': original_points},
            new_value={'user_points': new_points},
            remark=f'退款原因：{reason},{operation_desc}'
        )

    def create_distribution_income(self, order: ShopOrder) -> Dict[str, Any]:
        """
        创建分销收入记录

        参数:
            order: 订单对象

        返回:
            Dict[str, Any]: 包含处理结果的字典
        """
        from backend.mini_core.service import distribution_service, distribution_income_service,distribution_grade_service
        from backend.mini_core.domain.distribution import DistributionIncome
        # 获取当前下单用户信息
        user_id = order.user_id
        dis_user = distribution_service.get_by_user_id(user_id=user_id)
        if not dis_user:
            return dict(success=False, message="分销用户不存在", code=404)
        # 检查是否有分销上级
        user_father_id = dis_user.user_father_id
        # 获取上级用户信息
        parent_user = distribution_service.get_by_user_id(user_id=user_father_id)
        if not parent_user:
            return dict(success=False, message="上级用户不存在", code=404)
        user_father_id = parent_user.user_id
        # 获取上级用户的分销比率
        lv_id = parent_user.lv_id
        dis_grade_conf = distribution_grade_service.repo.get_by_id(lv_id)
        distribution_rate = dis_grade_conf.first_ratio
        if not distribution_rate or distribution_rate <= 0:
            return dict(success=False, message="分销比率无效", code=400)
        user_father_frozen_amount = parent_user.frozen_amount # 冻结金额
        user_father_frozen_amount= user_father_frozen_amount if user_father_frozen_amount else 0
        # 检查是否已经存在该订单的分销收入记录
        existing_income = distribution_income_service.repo.find(
            order_id=order.id,
            user_id=parent_user.user_id
        )
        if existing_income:
            return dict(success=False, message="分销收入记录已存在", code=400)

        # 计算分销收入
        order_amount = float(order.actual_amount)
        distribution_income_amount = order_amount * (float(distribution_rate) / 100)
        user_father_frozen_amount = user_father_frozen_amount + distribution_income_amount

        # 创建分销收入对象
        distribution_income = DistributionIncome(
            user_id=str(user_id),  # 获得分销收入的上级用户ID
            user_father_id = str(user_father_id),
            dis_name = dis_grade_conf.name,
            order_id=str(order.id),  # 订单ID
            order_no=order.order_no,  # 订单编号
            product_name=order.product_name,  # 产品名称
            money=order_amount,  # 订单金额
            distribution_amount=distribution_income_amount,  # 分销收入金额
            ratio=float(distribution_rate),  # 分销比例
            level=lv_id,  # 分销层级，默认1级
            status=3,  # 状态：0待入帐
            settlement_time=None,  # 结算时间，待结算时为空
            create_time=dt.datetime.now()
        )
        parent_user.frozen_amount  = user_father_frozen_amount
        self.repo.session.add(parent_user)
        self.repo.session.add(distribution_income)
        # 保存分销收入记录
        return None
