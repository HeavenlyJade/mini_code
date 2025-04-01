from typing import Type, Tuple

from sqlalchemy import Column, String, Table, Integer, DateTime, Numeric
import datetime as dt

from backend.extensions import mapper_registry
from backend.mini_core.domain.order.shop_order_setting import ShopOrderSetting
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['ShopOrderSettingSQLARepository']

# 订单配置表
shop_order_setting_table = Table(
    'shop_order_setting',
    mapper_registry.metadata,
    id_column(),
    Column('shop_id', Integer, nullable=False, comment='店铺ID'),
    Column('auto_close_minutes', Integer, comment='自动关闭(下单N分钟后未支付自动关闭订单)'),
    Column('auto_receive_days', Integer, comment='自动收货(发货后超过N天用户未确认,收货自动确认收货)'),
    Column('logistics_timeout_hours', Integer, comment='物流动态超时时未更新提醒(0代表不提醒)'),
    Column('points_rate', Numeric(10, 2), comment='积分抵扣比例(1元等于多少积分)'),
    Column('invoice_contact_phone', String(32), comment='联系电话'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('updater', String(64), comment='更新人'),
)

# 映射
mapper_registry.map_imperatively(ShopOrderSetting, shop_order_setting_table)


class ShopOrderSettingSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopOrderSetting]:
        return ShopOrderSetting

    @property
    def in_query_params(self) -> Tuple:
        return 'shop_id',

    def get_by_shop_id(self,) -> ShopOrderSetting:
        """
        获取指定店铺的订单配置

        Args:
            shop_id: 店铺ID

        Returns:
            ShopOrderSetting: 店铺订单配置
        """
        return self.find()
