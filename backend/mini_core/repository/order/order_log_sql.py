import datetime as dt
from typing import Type, Tuple, List, Dict, Any

from sqlalchemy import Column, String, Table, Integer, DateTime, Text, and_, or_, desc, BigInteger,JSON

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.order_log import OrderLog
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['OrderLogSQLARepository']

# 订单日志表
order_log_table = Table(
    'shop_order_log',
    mapper_registry.metadata,
    Column('id', BigInteger, primary_key=True, comment='主键ID'),
    Column('order_no', String(64), nullable=False, index=True, comment='订单编号'),
    Column('operation_type', String(32), nullable=False, comment='操作类型'),
    Column('operation_desc', String(255), nullable=False, comment='操作描述'),
    Column('operator', String(64), nullable=False, comment='操作人'),
    Column('operation_time', DateTime, nullable=False, comment='操作时间'),
    Column('operation_ip', String(64), comment='操作IP'),
    Column('old_value', JSON, comment='修改前值'),
    Column('new_value', JSON, comment='修改后值'),
    Column('remark', String(255), comment='备注'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
)

# 映射关系
mapper_registry.map_imperatively(OrderLog, order_log_table)


class OrderLogSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[OrderLog]:
        return OrderLog

    @property
    def in_query_params(self) -> Tuple:
        return 'order_no', 'operation_type', 'operator'

    @property
    def fuzzy_query_params(self) -> Tuple:
        return 'operation_desc', 'remark'

    @property
    def range_query_params(self) -> Tuple:
        return 'operation_time', 'create_time'

    def get_order_logs(self, order_no: str) -> List[OrderLog]:
        """获取指定订单的所有操作日志"""
        query = self.query().filter(OrderLog.order_no == order_no).order_by(desc(OrderLog.operation_time))
        return query.all()

    def get_order_logs_by_type(self, order_no: str, operation_type: str) -> List[OrderLog]:
        """获取指定订单的指定类型的操作日志"""
        query = self.query().filter(
            and_(OrderLog.order_no == order_no, OrderLog.operation_type == operation_type)
        ).order_by(desc(OrderLog.operation_time))
        return query.all()

    def get_operator_logs(self, operator: str, start_time: dt.datetime = None, end_time: dt.datetime = None) -> List[
        OrderLog]:
        """获取指定操作人的操作日志"""
        conditions = [OrderLog.operator == operator]

        if start_time:
            conditions.append(OrderLog.operation_time >= start_time)
        if end_time:
            conditions.append(OrderLog.operation_time <= end_time)

        query = self.query().filter(and_(*conditions)).order_by(desc(OrderLog.operation_time))
        return query.all()

    def get_latest_logs(self, limit: int = 50) -> List[OrderLog]:
        """获取最新的操作日志"""
        return self.query().order_by(desc(OrderLog.operation_time)).limit(limit).all()

    def search_logs(self, search_term: str) -> List[OrderLog]:
        """搜索操作日志"""
        search_pattern = f"%{search_term}%"
        query = self.query().filter(
            or_(
                OrderLog.operation_desc.like(search_pattern),
                OrderLog.remark.like(search_pattern),
                OrderLog.old_value.like(search_pattern),
                OrderLog.new_value.like(search_pattern)
            )
        ).order_by(desc(OrderLog.operation_time))
        return query.all()

    def get_statistics(self, start_time: dt.datetime = None, end_time: dt.datetime = None) -> Dict[str, Any]:
        """获取操作日志统计数据"""
        from sqlalchemy import func

        conditions = []
        if start_time:
            conditions.append(OrderLog.operation_time >= start_time)
        if end_time:
            conditions.append(OrderLog.operation_time <= end_time)

        base_query = self.session.query(OrderLog.operation_type, func.count(OrderLog.id))

        if conditions:
            base_query = base_query.filter(and_(*conditions))

        stats_by_type = base_query.group_by(OrderLog.operation_type).all()

        return {
            "total_logs": sum(count for _, count in stats_by_type),
            "logs_by_type": {op_type: count for op_type, count in stats_by_type}
        }
