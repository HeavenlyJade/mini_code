from typing import Type, Tuple

from sqlalchemy import Column, String, Table, Integer, DECIMAL, Text
from sqlalchemy import func

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
    Column('identity', Integer, comment='身份,0超级管理员，1，普通管理员，2，公司成员，3普通用户'),
    Column('reason', Integer, comment='原因'),
    Column('user_id', String(255), comment='用户ID'),
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
    Column('user_id', String(255), comment='用户ID'),
    Column('order_id', Integer, comment='订单ID'),
    Column('order_product_id', Integer, comment='产品订单ID'),
    Column('product_id', Integer, comment='产品ID'),
    Column('product_name', String(255), comment='产品名称'),
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
    Column('user_id', String(255), comment='变更对象'),
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

    def get_summary_tree(self, args):
        user_id = args["user_id"]
        ser_name = args.get("ser_name")

        if not ser_name:
            # 如果没有搜索条件，返回完整的树结构
            sql = """
                WITH RECURSIVE UserHierarchy AS (
                    SELECT *
                    FROM la_distribution
                    WHERE user_father_id = :user_id
                    UNION ALL
                    SELECT child.*
                    FROM la_distribution child
                    JOIN UserHierarchy parent ON child.user_father_id = parent.user_id
                )
                SELECT DISTINCT *
                FROM UserHierarchy
                ORDER BY user_father_id, id;
                """
            result = self.session.execute(sql, {'user_id': user_id}).fetchall()
        else:
            # 搜索匹配节点并获取其父节点路径
            sql = """
                WITH RECURSIVE UserHierarchy AS (
                    -- 获取所有子节点
                    SELECT *
                    FROM la_distribution
                    WHERE user_father_id = :user_id
                    UNION ALL
                    SELECT child.*
                    FROM la_distribution child
                    JOIN UserHierarchy parent ON child.user_father_id = parent.user_id
                ),
                -- 找出匹配名称的节点
                MatchedNodes AS (
                    SELECT *
                    FROM UserHierarchy
                    WHERE real_name LIKE :ser_name
                ),
                -- 找出匹配节点的所有父级ID（路径）
                ParentPaths AS (
                    SELECT user_father_id
                    FROM MatchedNodes
                    UNION
                    SELECT node.user_father_id
                    FROM la_distribution node
                    JOIN ParentPaths pp ON node.user_id = pp.user_father_id
                    WHERE node.user_father_id IS NOT NULL
                )
                -- 返回匹配节点及其父级路径上的所有节点
                SELECT DISTINCT h.*
                FROM UserHierarchy h
                WHERE h.real_name LIKE :ser_name
                   OR h.user_id IN (SELECT user_father_id FROM ParentPaths)
                ORDER BY h.user_father_id, h.id;
                """
            result = self.session.execute(sql, {
                'user_id': user_id,
                'ser_name': f"%{ser_name}%"
            }).fetchall()

        return [dict(i) for i in result]

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
    def query_params(self):
        return 'user_id',
    @property
    def range_query_params(self):
        return "settlement_time", "create_time"

    def get_money_sum_by_status(self, user_id: int) -> list:
        """
        使用ORM按状态分组统计指定用户的总收入金额

        参数:
            user_id: 用户ID

        返回:
            包含状态和对应总金额的列表
        """
        result = self.session.query(DistributionIncome.status,
                                    func.sum(DistributionIncome.money).label('total_money')) \
            .filter(DistributionIncome.user_id == user_id) \
            .group_by(DistributionIncome.status).all()
        return result

    def get_income_summary(self, user_id: int) -> dict:
        """
        获取用户的收益统计数据，包括今日收益、本月收益和累计收益

        参数:
            user_id: 用户ID

        返回:
            包含今日收益、本月收益和累计收益的字典
        """
        # 直接使用原生SQL
        sql = """
            SELECT
                IFNULL(SUM(CASE WHEN DATE(FROM_UNIXTIME(settlement_time)) = CURDATE() THEN money ELSE 0 END), 0) AS today_income,
                IFNULL(SUM(CASE WHEN DATE(FROM_UNIXTIME(settlement_time)) BETWEEN DATE_FORMAT(CURDATE(), '%Y-%m-01') AND LAST_DAY(CURDATE()) THEN money ELSE 0 END), 0) AS month_income,
                IFNULL(SUM(money), 0) AS total_income
            FROM la_distribution_income
            WHERE status = 1 AND user_id = :user_id
            """

        # 执行SQL
        result = self.session.execute(sql, {'user_id': user_id}).fetchone()

        # 返回结果
        return {
            'today_income': float(result[0]) if result else 0,
            'month_income': float(result[1]) if result else 0,
            'total_income': float(result[2]) if result else 0
        }


class DistributionLogSQLARepository(SQLARepository):
    @property
    def model(self) -> Type[DistributionLog]:
        return DistributionLog

    @property
    def in_query_params(self) -> Tuple:
        return 'distribution_id', 'change_object', 'change_type', 'source_id', 'admin_id'
