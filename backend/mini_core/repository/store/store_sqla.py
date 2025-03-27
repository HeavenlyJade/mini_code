from typing import Type, Tuple, List, Dict, Any
import datetime as dt

from sqlalchemy import Column, String, Table, Integer, DateTime, Text, Enum, Boolean, Numeric, func

from backend.extensions import mapper_registry
from backend.mini_core.domain.store import ShopStore
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['ShopStoreSQLARepository']

# 商店表
shop_store_table = Table(
    'shop_store',
    mapper_registry.metadata,
    id_column(),
    Column('name', String(128), nullable=False, comment='商店名称'),
    Column('type', String(32), comment='类型'),
    Column('store_code', String(32), comment='门店编号'),
    Column('fresh_delivery', String(128), comment='生鲜配送'),
    Column('receive_method', Enum('系统自动确认', '需要商家确认'), comment='接单模式'),
    Column('takeout_enabled', Boolean, default=False, comment='外卖模式'),
    Column('self_pickup_enabled', Boolean, default=False, comment='自取模式'),
    Column('dine_in_enabled', Boolean, default=False, comment='堂食模式'),
    Column('store_category', Integer, comment='门店分类ID'),
    Column('province', String(32), comment='省市区'),
    Column('address', String(255), comment='地址'),
    Column('contact_person', String(64), comment='联系人'),
    Column('contact_phone', String(20), comment='联系电话'),
    Column('is_public', Boolean, default=False, comment='是否公开服务方式'),
    Column('qq', String(20), comment='QQ'),
    Column('service_fee_rate', Numeric(10, 2), comment='服务费率'),
    Column('gst_tax_rate', Numeric(10, 2), comment='GST消费税率'),
    Column('print_config', Text, comment='打印打单'),
    Column('wechat_config', Text, comment='企业微信通知'),
    Column('business_scope', Text, comment='经营范围'),
    Column('description', Text, comment='介绍'),
    Column('features', Text, comment='特色'),
    Column('latitude', Numeric(10, 6), comment='地理位置纬度'),
    Column('longitude', Numeric(10, 6), comment='地理位置经度'),
    Column('sort_order', Integer, comment='排序'),
    Column('status', Enum('正常', '停用'), comment='状态'),
    Column('store_logo', Text, comment='商店Logo'),
    Column('store_image', Text, comment='商店图片'),
    Column('opening_hours', String(32), comment='营业时间'),
    Column('delivery_price', Numeric(10, 2), comment='配送价格'),
    Column('min_order_amount', Numeric(10, 2), comment='最小订单金额'),
    Column('door_info', String(255), comment='门店信息'),
    Column('wifi_name', String(64), comment='WiFi名称'),
    Column('wifi_password', String(64), comment='WiFi密码'),
    Column('customer_notice', Text, comment='客户须知'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
)

# 映射
mapper_registry.map_imperatively(ShopStore, shop_store_table)


class ShopStoreSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[ShopStore]:
        return ShopStore

    @property
    def in_query_params(self) -> Tuple:
        return 'name', 'type', 'store_code', 'store_category', 'province', 'status'

    @property
    def range_query_params(self) -> Tuple:
        return 'service_fee_rate', 'delivery_price', 'min_order_amount'

    def get_nearby_stores(self, latitude: float, longitude: float, distance: float = 5.0) -> List[Dict[str, Any]]:
        """
        获取附近的商店

        Args:
            latitude: 纬度
            longitude: 经度
            distance: 距离范围（公里）

        Returns:
            List[Dict[str, Any]]: 附近商店列表
        """
        # 使用地理位置计算距离的SQL
        # 这里使用了简化的计算方法，实际应用中可能需要更精确的地理位置计算
        sql = """
        SELECT *,
            (6371 * acos(cos(radians(:lat)) * cos(radians(latitude))
            * cos(radians(longitude) - radians(:lng))
            + sin(radians(:lat)) * sin(radians(latitude)))) AS distance
        FROM shop_store
        WHERE status = '正常'
        HAVING distance < :distance
        ORDER BY distance
        """

        result = self.session.execute(
            sql,
            {
                'lat': latitude,
                'lng': longitude,
                'distance': distance
            }
        ).fetchall()

        return [dict(row) for row in result]

    def get_stores_by_category(self, category_id: int) -> List[ShopStore]:
        """
        获取指定分类下的商店

        Args:
            category_id: 分类ID

        Returns:
            List[ShopStore]: 商店列表
        """
        return self.find(store_category=category_id, status='正常')

    def search_stores(self, keyword: str) -> List[ShopStore]:
        """
        搜索商店

        Args:
            keyword: 关键词

        Returns:
            List[ShopStore]: 搜索结果
        """
        # 使用LIKE进行模糊搜索
        query = self.query().filter(
            (ShopStore.name.like(f'%{keyword}%')) |
            (ShopStore.description.like(f'%{keyword}%')) |
            (ShopStore.features.like(f'%{keyword}%')) |
            (ShopStore.business_scope.like(f'%{keyword}%'))
        )
        return query.filter(ShopStore.status == '正常').all()

    def get_store_stats(self) -> Dict[str, Any]:
        """
        获取商店统计信息

        Returns:
            Dict[str, Any]: 统计信息
        """
        total = self.query().count()
        active = self.query().filter(ShopStore.status == '正常').count()
        inactive = self.query().filter(ShopStore.status == '停用').count()

        # 各种商店类型的数量
        type_stats = self.session.query(
            ShopStore.type,
            func.count(ShopStore.id).label('count')
        ).group_by(ShopStore.type).all()

        # 各省份商店数量
        province_stats = self.session.query(
            ShopStore.province,
            func.count(ShopStore.id).label('count')
        ).group_by(ShopStore.province).all()

        return {
            'total': total,
            'active': active,
            'inactive': inactive,
            'type_stats': [{'type': t[0], 'count': t[1]} for t in type_stats],
            'province_stats': [{'province': p[0], 'count': p[1]} for p in province_stats]
        }
