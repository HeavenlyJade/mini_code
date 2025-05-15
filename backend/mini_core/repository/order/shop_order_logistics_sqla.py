import datetime as dt
from typing import Type, Tuple, List, Dict, Any

from sqlalchemy import Column, String, Table, Integer, DateTime, Text, and_, or_, desc,JSON

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.shop_order_logistics import ShopOrderLogistics
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['ShopOrderLogisticsSQLARepository']

# 订单物流表
shop_order_logistics_table = Table(
    'shop_order_logistics',
    mapper_registry.metadata,
    id_column(),
    Column('order_no', String(30), nullable=False, index=True, comment='订单编号'),
    Column('logistics_no', String(50), nullable=False, comment='物流单号'),
    Column('logistics_company', String(50), nullable=False, comment='物流公司'),
    Column('courier_number', String(20), comment='快递员编号'),
    Column('courier_phone', String(15), comment='快递员电话'),
    Column('sender_info', JSON, comment='发件人信息(JSON格式)'),
    Column('receiver_info', JSON, nullable=False, comment='收件人信息(JSON格式)'),
    Column('shipping_time', DateTime, comment='发货时间'),
    Column('estimate_time', DateTime, comment='预计送达时间'),
    Column('receiving_time', DateTime, comment='实际收货时间'),
    Column('current_status', String(30), nullable=False, comment='当前状态'),
    Column('current_location', String(100), comment='当前位置'),
    Column('logistics_route', JSON, comment='物流轨迹(JSON格式)'),
    Column('remark', String(255), comment='备注'),
    Column('start_date', DateTime, nullable=False, comment='记录开始时间(用于控制表)'),
    Column('end_date', DateTime, comment='记录结束时间(用于控制表)'),
    Column('create_time', DateTime, nullable=False, default=dt.datetime.now),
    Column('update_time', DateTime, nullable=False, default=dt.datetime.now, onupdate=dt.datetime.now),
)

# 映射关系
mapper_registry.map_imperatively(ShopOrderLogistics, shop_order_logistics_table)


class ShopOrderLogisticsSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopOrderLogistics]:
        return ShopOrderLogistics

    @property
    def query_params(self) -> Tuple:
        return ('order_no', 'logistics_no', 'logistics_company', 'current_status')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('courier_number', 'courier_phone', 'current_location')

    @property
    def range_query_params(self) -> Tuple:
        return ('shipping_time', 'estimate_time', 'receiving_time', 'start_date', 'end_date', 'create_time')

    def get_by_order_no(self, order_no: str) -> ShopOrderLogistics:
        """
        通过订单编号获取物流信息

        Args:
            order_no: 订单编号

        Returns:
            ShopOrderLogistics: 订单物流信息
        """
        return self.find(order_no=order_no)

    def get_by_logistics_no(self, logistics_no: str) -> ShopOrderLogistics:
        """
        通过物流单号获取物流信息

        Args:
            logistics_no: 物流单号

        Returns:
            ShopOrderLogistics: 订单物流信息
        """
        return self.find(logistics_no=logistics_no)

    def get_con_logistics(self,kwargs: Dict[str, Any]):
        from sqlalchemy import and_
        import datetime as dt

        # 提取并移除特定参数
        current_status = kwargs.pop('current_status', '已发货')
        days = kwargs.pop('days', 7)

        # 计算指定天数前的日期
        days_ago = dt.datetime.now() - dt.timedelta(days=days)

        # 基础查询条件
        conditions = [
            # 状态为指定状态
            self.model.current_status == current_status,
            # 发货时间在指定天数内
            self.model.shipping_time >= days_ago,
        ]
        logistics_company = kwargs.get('logistics_company', None)
        order_no =kwargs.get('order_no', None)
        # 处理其他可选查询条件
        if logistics_company:
            conditions.append(self.model.logistics_company == logistics_company)

        if order_no:
            conditions.append(self.model.order_no == order_no)

        # 构建查询
        query = self.session.query(self.model).filter(and_(*conditions))
        query = query.order_by(self.model.shipping_time.desc())

        # 执行查询并返回结果
        return query.all()

    def get_active_logistics(self) -> List[ShopOrderLogistics]:
        """
        获取所有活跃的物流信息（尚未送达的）

        Returns:
            List[ShopOrderLogistics]: 活跃的物流信息列表
        """
        return self.session.query(ShopOrderLogistics).filter(
            ShopOrderLogistics.receiving_time.is_(None)).all()

    def update_logistics_route(self, logistics_id: int, args:dict) -> ShopOrderLogistics:
        """
        更新物流轨迹信息

        Args:
            logistics_id: 物流记录ID
            route_info: 物流轨迹信息(JSON字符串)

        Returns:
            ShopOrderLogistics: 更新后的物流信息
        """
        logistics = self.get_by_id(logistics_id)
        route_info= args.get('route_info', None)
        current_status = args.get("current_status",None)
        location = args.get("location")
        receiving_time =args.get("receiving_time")
        if logistics:
            if route_info:
                logistics.logistics_route = route_info
            if current_status:
                logistics.current_status = current_status
            if location:
                logistics.current_location = location
            if receiving_time:
                logistics.receiving_time = receiving_time
            logistics.update_time = dt.datetime.now()
            self.session.commit()
        return logistics

    def mark_as_delivered(self, logistics_id: int, receiving_time: dt.datetime = None) -> ShopOrderLogistics:
        """
        标记物流已送达

        Args:
            logistics_id: 物流记录ID
            receiving_time: 收货时间，默认为当前时间

        Returns:
            ShopOrderLogistics: 更新后的物流信息
        """
        logistics = self.get_by_id(logistics_id)
        if logistics:
            logistics.current_status = '已送达'
            logistics.receiving_time = receiving_time or dt.datetime.now()
            logistics.end_date = dt.datetime.now()
            self.session.commit()
        return logistics

    def get_logistics_by_date_range(self, start_date: dt.datetime, end_date: dt.datetime) -> List[ShopOrderLogistics]:
        """
        获取指定日期范围内的物流信息

        Args:
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            List[ShopOrderLogistics]: 符合条件的物流信息列表
        """
        return self.session.query(ShopOrderLogistics).filter(
            and_(
                ShopOrderLogistics.shipping_time >= start_date,
                ShopOrderLogistics.shipping_time <= end_date
            )
        ).order_by(desc(ShopOrderLogistics.shipping_time)).all()
