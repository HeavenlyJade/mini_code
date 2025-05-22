from typing import Type, Tuple, List, Dict, Any
from decimal import Decimal
import datetime as dt

from sqlalchemy import Column, String, Table, Integer, DateTime, Text, Boolean, DECIMAL
from sqlalchemy import func, and_, or_, desc

from backend.extensions import mapper_registry
from backend.mini_core.domain.member_level import MemberLevelConfig
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['MemberLevelConfigSQLARepository']

# 会员等级配置表
member_level_config_table = Table(
    'member_level_config',
    mapper_registry.metadata,
    id_column(),
    Column('level_code', String(20), nullable=False, unique=True, comment='等级代码'),
    Column('level_name', String(50), nullable=False, comment='等级名称'),
    Column('level_value', Integer, nullable=False, comment='等级数值'),
    Column('upgrade_condition_type', Integer, default=1,
           comment='升级条件类型：1-消费金额 2-消费次数 3-邀请人数 4-手动设置'),
    Column('upgrade_amount', DECIMAL(10, 2), default=0.00, comment='升级所需消费金额'),
    Column('upgrade_count', Integer, default=0, comment='升级所需消费次数'),
    Column('upgrade_invite_count', Integer, default=0, comment='升级所需邀请人数'),
    Column('discount_rate', DECIMAL(5, 2), default=100.00, comment='会员折扣率'),
    Column('point_ratio', DECIMAL(5, 2), default=1.00, comment='积分倍率'),
    Column('level_icon', String(255), comment='等级图标URL'),
    Column('level_color', String(20), comment='等级颜色'),
    Column('level_description', Text, comment='等级描述'),
    Column('benefits', Text, comment='会员权益(JSON格式)'),
    Column('is_enabled', Boolean, default=True, comment='是否启用'),
    Column('sort_order', Integer, default=0, comment='排序'),
    Column('create_time', DateTime, default=dt.datetime.now),
    Column('update_time', DateTime, default=dt.datetime.now, onupdate=dt.datetime.now),
    Column('creator', String(64), comment='创建人'),
    Column('updater', String(64), comment='更新人'),
)

# 映射关系
mapper_registry.map_imperatively(MemberLevelConfig, member_level_config_table)


class MemberLevelConfigSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[MemberLevelConfig]:
        return MemberLevelConfig

    @property
    def query_params(self) -> Tuple:
        return ('level_code', 'level_name', 'upgrade_condition_type', 'is_enabled')

    @property
    def fuzzy_query_params(self) -> Tuple:
        return ('level_name', 'level_description')

    @property
    def range_query_params(self) -> Tuple:
        return ('level_value', 'upgrade_amount', 'discount_rate', 'point_ratio', 'create_time', 'update_time')

    def get_by_level_code(self, level_code: str) -> MemberLevelConfig:
        """
        根据等级代码获取等级配置

        Args:
            level_code: 等级代码

        Returns:
            MemberLevelConfig: 等级配置对象
        """
        return self.find(level_code=level_code)

    def get_by_level_value(self, level_value: int) -> MemberLevelConfig:
        """
        根据等级数值获取等级配置

        Args:
            level_value: 等级数值

        Returns:
            MemberLevelConfig: 等级配置对象
        """
        return self.find(level_value=level_value)

    def get_enabled_levels(self) -> List[MemberLevelConfig]:
        """
        获取所有已启用的会员等级，按排序排列

        Returns:
            List[MemberLevelConfig]: 已启用的等级列表
        """
        return self.session.query(self.model).filter(
            self.model.is_enabled == True
        ).order_by(self.model.sort_order, self.model.level_value).all()



    def check_level_code_exists(self, level_code: str, exclude_id: int = None) -> bool:
        """
        检查等级代码是否已存在

        Args:
            level_code: 等级代码
            exclude_id: 排除的ID（用于更新时检查）

        Returns:
            bool: 是否存在
        """
        query = self.session.query(self.model).filter(
            self.model.level_code == level_code
        )

        if exclude_id:
            query = query.filter(self.model.id != exclude_id)

        return query.first() is not None
