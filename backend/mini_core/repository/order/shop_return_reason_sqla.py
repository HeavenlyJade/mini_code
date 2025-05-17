from typing import Type, Tuple, List

from sqlalchemy import Column, String, Table, Integer, DateTime, Boolean
import datetime as dt

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.shop_return_reason import ShopReturnReason
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['ShopReturnReasonSQLARepository']

# 退货原因设置表
shop_return_reason_table = Table(
    'shop_return_reason',
    mapper_registry.metadata,
    id_column(),
    Column('reason_type', String(64), nullable=False, comment='原因类型'),
    Column('sort_order', Integer, default=1, comment='排序'),
    Column('is_enabled', Boolean, default=True, comment='是否可用'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
)

# 映射
mapper_registry.map_imperatively(ShopReturnReason, shop_return_reason_table)


class ShopReturnReasonSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopReturnReason]:
        return ShopReturnReason

    @property
    def query_params(self) -> Tuple:
        return 'is_enabled',

    @property
    def fuzzy_query_params(self) -> Tuple:
        return 'reason_type',

    def get_enabled_reasons(self) -> List[ShopReturnReason]:
        """
        获取所有启用的退货原因

        Returns:
            List[ShopReturnReason]: 启用的退货原因列表，按排序字段排序
        """
        query = self.query().filter(ShopReturnReason.is_enabled == True)
        query = query.order_by(ShopReturnReason.sort_order)
        return query.all()

    def update_status(self, reason_id: int, is_enabled: bool) -> ShopReturnReason:
        """
        更新退货原因的启用状态

        Args:
            reason_id: 退货原因ID
            is_enabled: 是否启用

        Returns:
            ShopReturnReason: 更新后的退货原因对象
        """
        reason = self.get_by_id(reason_id)
        if reason:
            reason.is_enabled = is_enabled
            self.session.commit()
        return reason

    def update_sort_order(self, reason_id: int, sort_order: int) -> ShopReturnReason:
        """
        更新退货原因的排序

        Args:
            reason_id: 退货原因ID
            sort_order: 排序值

        Returns:
            ShopReturnReason: 更新后的退货原因对象
        """
        reason = self.get_by_id(reason_id)
        if reason:
            reason.sort_order = sort_order
            self.session.commit()
        return reason
