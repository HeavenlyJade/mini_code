import datetime as dt
from typing import Type, Tuple

from flask_jwt_extended import get_current_user
from sqlalchemy import Column, String, Table, Integer, DateTime, or_, and_, DECIMAL, Text

from backend.extensions import mapper_registry
from backend.mini_core.domain.distribution import (Distribution, DistributionConfig,
                                                   DistributionGrade, DistributionGradeUpdate,
                                                   DistributionIncome, DistributionLog)
from kit.repository.sqla import SQLARepository
from kit.util.sqla import id_column

__all__ = ['DistributionSQLARepository', 'DistributionConfigSQLARepository',
           'DistributionGradeSQLARepository', 'DistributionGradeUpdateSQLARepository',
           'DistributionIncomeSQLARepository', 'DistributionLogSQLARepository']

# 分销表
distribution_table = Table(
    'la_distribution',
    mapper_registry.metadata,
    id_column(),
    Column('sn', String(50), comment='编号'),
    Column('real_name', String(50), comment='真实姓名'),
    Column('mobile', String(20), comment='手机号'),
    Column('identity', Integer, comment='身份'),
    Column('reason', Integer, comment='原因'),
    Column('user_id', Integer, comment='用户ID'),
    Column('user_father_id', Integer, comment='上级ID'),
    Column('grade_id', Integer, comment='等级ID'),
    Column('remark', String(255), comment='备注'),
    Column('status', Integer, comment='状态 (0-未审核, 1-已审核)'),
    Column('audit_time', Integer, comment='审核时间'),
    Column('create_time', Integer, comment='创建时间'),
    Column('update_time', Integer, comment='更新时间'),
    Column('delete_time', Integer, comment='删除时间'),
)

# 分销配置表
distribution_config_table = Table(
    'la_distribution_config',
    mapper_registry.metadata,
    id_column(),
    Column('key', String(50), comment='配置项'),
    Column('remake', String(255), comment=''),
    Column('value', String(255), comment='配置值'),
    Column('create_time', Integer, comment='创建时间'),
    Column('update_time', Integer, comment='更新时间'),
    Column('delete_time', Integer, comment='删除时间'),
)

# 分销等级表
distribution_grade_table = Table(
    'la_distribution_grade',
    mapper_registry.metadata,
    id_column(),
    Column('name', String(50), comment='等级名称'),
    Column('weight', Integer, comment='权重'),
    Column('self_ratio', DECIMAL(10, 2), comment='自购比例'),
    Column('first_ratio', DECIMAL(10, 2), comment='一级分拥比例'),
    Column('second_ratio', DECIMAL(10, 2), comment='二级分拥比例'),
    Column('remark', String(255), comment='备注'),
    Column('update_relation', Integer, comment='分销关系'),
    Column('create_time', Integer, comment='创建时间'),
    Column('update_time', Integer, comment='更新时间'),
    Column('delete_time', Integer, comment='删除时间'),
)

# 分销等级更新条件表
distribution_grade_update_table = Table(
    'la_distribution_grade_update',
    mapper_registry.metadata,
    id_column(),
    Column('grade_id', Integer, comment='等级ID'),
    Column('key', String(50), comment='条件名称'),
    Column('remake', String(255), comment=''),
    Column('value', DECIMAL(10, 2), comment='条件值'),
    Column('create_time', Integer, comment='创建时间'),
    Column('update_time', Integer, comment='更新时间'),
    Column('delete_time', Integer, comment='删除时间'),
)

# 分销收入表
distribution_income_table = Table(
    'la_distribution_income',
    mapper_registry.metadata,
    id_column(),
    Column('user_id', Integer, comment='用户ID'),
    Column('order_id', Integer, comment='订单ID'),
    Column('order_product_id', Integer, comment='产品订单ID'),
    Column('product_id', Integer, comment='产品ID'),
    Column('item_id', Integer, comment='商品ID'),
    Column('money', DECIMAL(10, 2), comment='金额'),
    Column('grade_id', Integer, comment='分销等级ID'),
    Column('level', Integer, comment='分销层级'),
    Column('ratio', DECIMAL(10, 2), comment='分销比例'),
    Column('status', Integer, comment='状态,0：待结算，2:已结算,3冻结'),
    Column('settlement_time', Integer, comment='结算时间'),
    Column('create_time', Integer, comment='创建时间'),
    Column('update_time', Integer, comment='更新时间'),
    Column('delete_time', Integer, comment='删除时间'),
)

# 分销日志表
distribution_log_table = Table(
    'la_distribution_log',
    mapper_registry.metadata,
    id_column(),
    Column('distribution_id', Integer, comment='分销ID'),
    Column('change_object', String(50), comment='变更对象'),
    Column('change_type', String(50), comment='变更类型'),
    Column('source_id', Integer, comment='来源ID'),
    Column('action', String(50), comment='操作'),
    Column('before_amount', DECIMAL(10, 2), comment='变更前金额'),
    Column('left_amount', DECIMAL(10, 2), comment='剩余金额'),
    Column('source_sn', String(50), comment='来源单号'),
    Column('extra', Text, comment='额外信息'),
    Column('admin_id', Integer, comment='管理员ID'),
    Column('create_time', Integer, comment='创建时间'),
    Column('update_time', Integer, comment='更新时间'),
    Column('delete_time', Integer, comment='删除时间'),
)

# 映射关系
mapper_registry.map_imperatively(Distribution, distribution_table)
mapper_registry.map_imperatively(DistributionConfig, distribution_config_table)
mapper_registry.map_imperatively(DistributionGrade, distribution_grade_table)
mapper_registry.map_imperatively(DistributionGradeUpdate, distribution_grade_update_table)
mapper_registry.map_imperatively(DistributionIncome, distribution_income_table)
mapper_registry.map_imperatively(DistributionLog, distribution_log_table)


class DistributionSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[Distribution]:
        return Distribution

    @property
    def in_query_params(self) -> Tuple:
        return 'sn', 'real_name', 'mobile', 'user_id', 'grade_id', 'status'


class DistributionConfigSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[DistributionConfig]:
        return DistributionConfig

    @property
    def in_query_params(self) -> Tuple:
        return 'key',


class DistributionGradeSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[DistributionGrade]:
        return DistributionGrade

    @property
    def in_query_params(self) -> Tuple:
        return 'name',


class DistributionGradeUpdateSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[DistributionGradeUpdate]:
        return DistributionGradeUpdate

    @property
    def in_query_params(self) -> Tuple:
        return 'grade_id', 'key'


class DistributionIncomeSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[DistributionIncome]:
        return DistributionIncome

    @property
    def in_query_params(self) -> Tuple:
        return 'user_id', 'order_id', 'product_id', 'grade_id', 'status'


class DistributionLogSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[DistributionLog]:
        return DistributionLog

    @property
    def in_query_params(self) -> Tuple:
        return 'distribution_id', 'change_object', 'change_type', 'source_id', 'admin_id'
