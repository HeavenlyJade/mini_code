import datetime as dt
import json
from typing import Dict, Any, List, Optional
from flask_jwt_extended import get_current_user
from flask import g

from kit.service.base import CRUDService
from backend.mini_core.domain.order.shop_order_logistics import ShopOrderLogistics
from backend.mini_core.repository.order.shop_order_logistics_sqla import ShopOrderLogisticsSQLARepository

__all__ = ['ShopOrderLogisticsService']


class ShopOrderLogisticsService(CRUDService[ShopOrderLogistics]):
    def __init__(self, repo: ShopOrderLogisticsSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> ShopOrderLogisticsSQLARepository:
        return self._repo

    def get_logistics_list(self, args: dict) -> Dict[str, Any]:
        """
        获取物流信息列表，支持分页和筛选

        Args:
            args: 查询参数，可包含以下内容:
                - order_no: 订单编号
                - logistics_no: 物流单号
                - logistics_company: 物流公司
                - current_status: 当前状态
                - shipping_time: 发货时间范围
                - page: 页码
                - size: 每页条数

        Returns:
            Dict: 包含物流信息列表和总数的字典
        """
        # 处理时间范围查询
        if 'shipping_start_time' in args and 'shipping_end_time' in args:
            args['shipping_time'] = [args.pop('shipping_start_time'), args.pop('shipping_end_time')]

        if 'estimate_start_time' in args and 'estimate_end_time' in args:
            args['estimate_time'] = [args.pop('estimate_start_time'), args.pop('estimate_end_time')]

        if 'receiving_start_time' in args and 'receiving_end_time' in args:
            args['receiving_time'] = [args.pop('receiving_start_time'), args.pop('receiving_end_time')]

        data, total = self._repo.list(**args)
        return dict(data=data, total=total, code=200)

    def get_logistics_by_id(self, logistics_id: int) -> Dict[str, Any]:
        """
        通过ID获取物流信息

        Args:
            logistics_id: 物流信息ID

        Returns:
            Dict: 包含物流信息的字典
        """
        data = self._repo.get_by_id(logistics_id)
        if not data:
            return dict(data=None, code=404, message="物流信息不存在")
        return dict(data=data, code=200)

    def get_logistics_by_order_no(self, order_no: str) -> Dict[str, Any]:
        """
        通过订单编号获取物流信息

        Args:
            order_no: 订单编号

        Returns:
            Dict: 包含物流信息的字典
        """
        data = self._repo.get_by_order_no(order_no)
        if not data:
            return dict(data=None, code=404, message="订单物流信息不存在")
        return dict(data=data, code=200)

    def get_logistics_by_logistics_no(self, logistics_no: str) -> Dict[str, Any]:
        """
        通过物流单号获取物流信息

        Args:
            logistics_no: 物流单号

        Returns:
            Dict: 包含物流信息的字典
        """
        data = self._repo.get_by_logistics_no(logistics_no)
        if not data:
            return dict(data=None, code=404, message="物流信息不存在")
        return dict(data=data, code=200)

    def create_logistics(self, logistics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建物流信息

        Args:
            logistics_data: 物流信息数据，包含以下内容:
                - order_no: 订单编号
                - logistics_no: 物流单号
                - logistics_company: 物流公司
                - sender_info: 发件人信息(JSON格式)
                - receiver_info: 收件人信息(JSON格式)
                等

        Returns:
            Dict: 包含创建结果的字典
        """
        # 检查必要字段
        required_fields = ['order_no', 'logistics_no', 'logistics_company', 'receiver_info', 'current_status']
        for field in required_fields:
            if field not in logistics_data or not logistics_data[field]:
                return dict(data=None, code=400, message=f"缺少必要字段: {field}")

        # 检查订单物流是否已存在
        existing = self._repo.get_by_order_no(logistics_data['order_no'])
        if existing:
            return dict(data=None, code=400, message="订单物流信息已存在")

        # 设置初始状态
        if 'current_status' not in logistics_data:
            logistics_data['current_status'] = '待发货'

        # 设置记录开始时间
        if 'start_date' not in logistics_data:
            logistics_data['start_date'] = dt.datetime.now()

        # 创建物流信息
        logistics = ShopOrderLogistics(**logistics_data)
        self._set_updater(logistics)
        result = self._repo.create(logistics)
        return dict(data=result, code=200, message="物流信息创建成功")

    def update_logistics(self, logistics_id: int, logistics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新物流信息

        Args:
            logistics_id: 物流信息ID
            logistics_data: 更新的物流信息数据

        Returns:
            Dict: 包含更新结果的字典
        """
        existing = self._repo.get_by_id(logistics_id)
        if not existing:
            return dict(data=None, code=404, message="物流信息不存在")

        # 防止修改关键字段
        if 'order_no' in logistics_data and logistics_data['order_no'] != existing.order_no:
            return dict(data=None, code=400, message="订单编号不允许修改")

        # 更新物流信息
        self._set_updater(existing)
        result = self._repo.update(logistics_id, ShopOrderLogistics(**logistics_data))
        return dict(data=result, code=200, message="物流信息更新成功")

    def update_logistics_status(self, logistics_id: int, status: str, location: str = None) -> Dict[str, Any]:
        """
        更新物流状态

        Args:
            logistics_id: 物流信息ID
            status: 新的物流状态
            location: 当前位置

        Returns:
            Dict: 包含更新结果的字典
        """
        logistics = self._repo.get_by_id(logistics_id)
        if not logistics:
            return dict(data=None, code=404, message="物流信息不存在")

        # 更新状态和位置
        result = self._repo.update_logistics_status(logistics_id, status, location)

        # 记录状态变更到物流轨迹
        self._add_to_logistics_route(logistics_id, {
            'time': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': status,
            'location': location or logistics.current_location,
            'remark': f'状态更新为: {status}'
        })

        return dict(data=result, code=200, message="物流状态更新成功")

    def mark_as_shipped(self, logistics_id: int, shipping_time: dt.datetime = None) -> Dict[str, Any]:
        """
        标记物流为已发货

        Args:
            logistics_id: 物流信息ID
            shipping_time: 发货时间，默认为当前时间

        Returns:
            Dict: 包含更新结果的字典
        """
        logistics = self._repo.get_by_id(logistics_id)
        if not logistics:
            return dict(data=None, code=404, message="物流信息不存在")

        # 更新发货信息
        logistics.shipping_time = shipping_time or dt.datetime.now()
        logistics.current_status = '已发货'
        self._set_updater(logistics)
        self._repo.update(logistics_id, logistics)

        # 记录发货到物流轨迹
        self._add_to_logistics_route(logistics_id, {
            'time': logistics.shipping_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': '已发货',
            'location': logistics.current_location,
            'remark': '订单已发货'
        })

        return dict(data=logistics, code=200, message="订单已标记为已发货")

    def mark_as_delivered(self, logistics_id: int, receiving_time: dt.datetime = None) -> Dict[str, Any]:
        """
        标记物流为已送达

        Args:
            logistics_id: 物流信息ID
            receiving_time: 收货时间，默认为当前时间

        Returns:
            Dict: 包含更新结果的字典
        """
        result = self._repo.mark_as_delivered(logistics_id, receiving_time)
        if not result:
            return dict(data=None, code=404, message="物流信息不存在")

        # 记录送达到物流轨迹
        delivery_time = receiving_time or dt.datetime.now()
        self._add_to_logistics_route(logistics_id, {
            'time': delivery_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': '已送达',
            'location': result.current_location,
            'remark': '订单已送达'
        })

        return dict(data=result, code=200, message="订单已标记为已送达")

    def delete_logistics(self, logistics_id: int) -> Dict[str, Any]:
        """
        删除物流信息

        Args:
            logistics_id: 物流信息ID

        Returns:
            Dict: 包含删除结果的字典
        """
        logistics = self._repo.get_by_id(logistics_id)
        if not logistics:
            return dict(data=None, code=404, message="物流信息不存在")

        self._repo.delete(logistics_id)
        return dict(code=200, message="物流信息删除成功")

    def get_active_logistics(self) -> Dict[str, Any]:
        """
        获取所有活跃的物流信息（尚未送达的）

        Returns:
            Dict: 包含活跃物流信息的字典
        """
        data = self._repo.get_active_logistics()
        return dict(data=data, code=200, total=len(data))

    def get_logistics_by_date_range(self, start_date: dt.datetime, end_date: dt.datetime) -> Dict[str, Any]:
        """
        获取指定日期范围内的物流信息

        Args:
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            Dict: 包含符合条件的物流信息的字典
        """
        data = self._repo.get_logistics_by_date_range(start_date, end_date)
        return dict(data=data, code=200, total=len(data))

    def _add_to_logistics_route(self, logistics_id: int, route_item: Dict[str, Any]) -> None:
        """
        添加物流轨迹记录

        Args:
            logistics_id: 物流信息ID
            route_item: 轨迹项，包含时间、状态、位置和备注
        """
        logistics = self._repo.get_by_id(logistics_id)
        if not logistics:
            return

        # 解析现有轨迹
        route = []
        if logistics.logistics_route:
            try:
                route = json.loads(logistics.logistics_route)
            except:
                route = []

        # 确保route是列表
        if not isinstance(route, list):
            route = []

        # 添加新轨迹
        route.append(route_item)

        # 更新轨迹
        self._repo.update_logistics_route(logistics_id, json.dumps(route))

    def _set_updater(self, entity: ShopOrderLogistics) -> None:
        """设置更新者"""
        if hasattr(g, 'creator'):
            entity.updater = g.creator
        else:
            current_user = get_current_user()
            if hasattr(current_user, 'username'):
                entity.updater = current_user.username
