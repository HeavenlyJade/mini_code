import datetime as dt
import json
from typing import Type, Tuple, List,Dict

from sqlalchemy import Column, String, Table, Integer, Numeric, Text, and_,DateTime

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.order_detail import OrderDetail
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['OrderDetailSQLARepository']

# 订单详情表
order_detail_table = Table(
    'shop_order_shop_detail',
    mapper_registry.metadata,
    id_column(),
    Column('order_item_id', String(255), nullable=False, index=True, comment='订单明细ID'),
    Column('order_no', String(255), nullable=False, index=True, comment='订单ID'),
    Column('sku_id', String(255), nullable=False, comment='sku_id'),
    Column('product_id', Integer, comment='商品ID'),
    Column('sku_code', String(64), comment='SKU编码'),
    Column('price', Numeric(10, 2), nullable=False, comment='原价格'),
    Column('actual_price', Numeric(10, 2), nullable=False, comment='实际购买价格'),
    Column('num', Integer, nullable=False, comment='购买数量'),
    Column('product_img', String(255), comment='商品图片'),
    Column('product_spec', String(255), comment='商品规格'),
    Column('product_name', String(255), comment='商品名称'),
    Column('refund_status', String(32), comment='退款状态'),
    Column('quantity', Integer, comment='商品数量'),
    Column('unit_price', Numeric(10, 2), comment='商品单价'),
    Column('total_price', Numeric(10, 2), comment='商品总价'),
    Column('is_gift', Integer, default=0, comment='是否赠品'),
    Column('refund_status', Integer, default=0, comment='退款状态,0:无退款,1退款中,2，已拒绝,3，已完成'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('refund_time', DateTime, comment='退款申请时间1'),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

# 映射关系
mapper_registry.map_imperatively(OrderDetail, order_detail_table)


class OrderDetailSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[OrderDetail]:
        return OrderDetail

    @property
    def query_params(self) -> Tuple:
        return 'refund_status','order_no', 'sku_id', 'product_id', 'sku_code'

    @property
    def fuzzy_query_params(self) -> Tuple:
        return 'product_name',

    def get_order_details(self, order_no: str) -> Dict:
        """
        获取指定订单的所有相关信息，包括订单详情、订单主信息和操作日志

        Args:
            order_no: 订单编号

        Returns:
            包含订单详情、订单主信息和操作日志的字典
        """
        # 查询订单详情
        detail_sql = """ SELECT * FROM shop_order_shop_detail WHERE order_no = :order_no """
        order_details = self.session.execute(detail_sql, {'order_no': order_no}).fetchall()

        # 查询订单主信息
        order_sql = """ SELECT * FROM shop_order WHERE order_no = :order_no """
        order_info = self.session.execute(order_sql, {'order_no': order_no}).fetchone()

        # 查询订单操作日志
        log_sql = """ SELECT * FROM shop_order_log WHERE order_no = :order_no ORDER BY operation_time DESC """
        order_logs = self.session.execute(log_sql, {'order_no': order_no}).fetchall()

        # 构建结果(将每行记录转换为字典)
        re_order_logs = []
        for row in order_logs:
            old_value = row.old_value
            new_value = row.new_value
            re_data = dict(row)
            if old_value and isinstance(old_value, str):
                re_data["old_value"] = json.loads(old_value)
            if new_value and isinstance(new_value, str):
                re_data["new_value"] = json.loads(new_value)
            re_order_logs.append(re_data)
        result = {
            "order_details": [dict(row) for row in order_details],
            "order_info": dict(order_info) if order_info else None,
            "order_logs": re_order_logs
        }

        return result


    def batch_create_details(self, details: List[OrderDetail]) -> None:
        """批量创建订单详情"""
        self.create_many(details)

    def get_gift_details(self, order_no: str) -> List[OrderDetail]:
        """获取指定订单的所有赠品详情"""
        query = self.session.query().filter(
            and_(OrderDetail.order_no == order_no, OrderDetail.is_gift == 1)
        )
        return query.all()
