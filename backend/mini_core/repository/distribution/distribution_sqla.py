from typing import Type, Tuple,List,Dict

from sqlalchemy import Column, String, Table, Integer, DECIMAL, Text,DateTime,Float
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
    Column("lv_id",Integer,comment="用户等级ID"),
    Column('identity', Integer, comment='身份,0超级管理员，1，普通管理员，2，公司成员，3普通用户'),
    Column('reason', Integer, comment='原因'),
    Column('wait_amount', Float, comment='已提现金额'),
    Column('total_amount', Float, comment='待提现金额'),
    Column('withdrawn_amount', Float, comment='总金额'),
    Column('user_id', String(255), comment='用户ID'),
    Column('user_father_id', Integer, comment='上级ID'),
    Column('grade_id', Integer, comment='等级ID'),
    Column('remark', String(255), comment='备注'),
    Column('status', Integer, comment='状态 (0-未审核, 1-已审核)'),
    Column('audit_time', DateTime, comment='审核时间'),
    Column('create_time', DateTime, comment='创建时间'),
    Column('update_time', DateTime, comment='更新时间'),
    Column('delete_time', DateTime, comment='删除时间'),
)

# 分销配置表
distribution_config_table = Table(
    'la_distribution_config',
    mapper_registry.metadata,
    id_column(),
    Column('key', String(50), comment='配置项'),
    Column('remake', String(255), comment=''),
    Column('value', String(255), comment='配置值'),
    Column('content', Text, comment=''),
    Column('title', String(255), comment=''),
    Column('create_time', DateTime, comment='创建时间'),
    Column('update_time', DateTime, comment='更新时间'),
    Column('delete_time', DateTime, comment='删除时间'),
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
    Column('conditions', Float,comment='扽就条件'),

    Column('remark', String(255), comment='备注'),
    Column('update_relation', Integer, comment='分销关系'),
    Column('create_time', DateTime, comment='创建时间'),
    Column('update_time', DateTime, comment='更新时间'),
    Column('delete_time', DateTime, comment='删除时间'),
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
    Column('create_time', DateTime, comment='创建时间'),
    Column('update_time', DateTime, comment='更新时间'),
    Column('delete_time', DateTime, comment='删除时间'),
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
    Column('settlement_time', DateTime, comment='结算时间'),
    Column('create_time', DateTime, comment='创建时间'),
    Column('update_time', DateTime, comment='更新时间'),
    Column('delete_time', DateTime, comment='删除时间'),
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
    Column('create_time', DateTime, comment='创建时间'),
    Column('update_time', DateTime, comment='更新时间'),
    Column('delete_time', DateTime, comment='删除时间'),
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
    def query_params(self) -> Tuple:
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

    def list_with_parent_info(self, **kwargs) -> Tuple[List[Dict], int]:
        """
        获取分销用户列表，并包含上级用户的名称信息

        参数:
            与list方法相同的查询参数（页码、每页数量、过滤条件等）

        返回:
            包含上级用户名称的分销用户列表及总数
        """
        # 构建基础SQL查询
        base_sql = """
            SELECT d.*, parent.real_name as parent_name
            FROM la_distribution d
            LEFT JOIN la_distribution parent ON d.user_father_id = parent.user_id
            WHERE 1=1
        """

        # 构建WHERE条件
        params = {}
        where_clauses = []

        # 添加查询条件
        if 'sn' in kwargs and kwargs['sn']:
            where_clauses.append("d.sn = :sn")
            params['sn'] = kwargs['sn']

        if 'real_name' in kwargs and kwargs['real_name']:
            where_clauses.append("d.real_name LIKE :real_name")
            params['real_name'] = f"%{kwargs['real_name']}%"

        if 'mobile' in kwargs and kwargs['mobile']:
            where_clauses.append("d.mobile LIKE :mobile")
            params['mobile'] = f"%{kwargs['mobile']}%"

        if 'user_id' in kwargs and kwargs['user_id']:
            where_clauses.append("d.user_id = :user_id")
            params['user_id'] = kwargs['user_id']

        if 'grade_id' in kwargs and kwargs['grade_id']:
            where_clauses.append("d.grade_id = :grade_id")
            params['grade_id'] = kwargs['grade_id']

        if 'status' in kwargs and kwargs['status'] is not None:
            where_clauses.append("d.status = :status")
            params['status'] = kwargs['status']

        # 处理时间范围查询
        if 'create_time' in kwargs and isinstance(kwargs['create_time'], list) and len(kwargs['create_time']) == 2:
            start_time, end_time = kwargs['create_time']
            where_clauses.append("d.create_time BETWEEN :start_time AND :end_time")
            params['start_time'] = start_time
            params['end_time'] = end_time

        # 拼接WHERE条件
        if where_clauses:
            base_sql += " AND " + " AND ".join(where_clauses)

        # 添加排序
        if 'ordering' in kwargs and kwargs['ordering']:
            order_fields = []
            for field in kwargs['ordering']:
                is_desc = field.startswith('-')
                field_name = field[1:] if is_desc else field
                order_fields.append(f"d.{field_name} {'DESC' if is_desc else 'ASC'}")

            if order_fields:
                base_sql += " ORDER BY " + ", ".join(order_fields)
        else:
            # 默认排序
            base_sql += " ORDER BY d.create_time DESC"

        # 计算总数
        count_sql = f"""
            SELECT COUNT(*) as total
            FROM la_distribution d
            WHERE {' AND '.join(where_clauses) if where_clauses else '1=1'}
        """
        total = 0
        if kwargs.get('need_total_count'):
            total_row = self.session.execute(count_sql, params).fetchone()
            total = total_row.total if total_row else 0

        # 添加分页
        if 'page' in kwargs and 'size' in kwargs:
            page = int(kwargs['page'])
            size = int(kwargs['size'])
            base_sql += f" LIMIT {size} OFFSET {(page - 1) * size}"

        # 执行查询
        result = self.session.execute(base_sql, params).fetchall()

        # 将结果转换为字典列表
        result_list = [dict(row) for row in result]


        return result_list, total
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
    def query_params(self) -> Tuple:
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
        return 'user_id',"status","product_name"
    @property
    def range_query_params(self):
        return "settlement_time", "create_time"

    def get_money_sum_by_status(self, args: dict = None) -> list:
        """
        使用ORM按状态分组统计收入金额和订单数，支持多种筛选条件

        参数:
            args: 包含查询条件的字典，可以包含以下键:
                - user_id: 用户ID
                - order_id: 订单ID
                - status: 状态码
                - start_time: 创建时间开始范围
                - end_time: 创建时间结束范围

        返回:
            包含状态、总金额和订单数的列表
        """
        # 确保args是一个字典
        args = args or {}

        # 构建基础查询 - 包括状态、总金额和订单数
        query = self.session.query(
            DistributionIncome.status,
            func.sum(DistributionIncome.money).label('total_money'),
            func.count(DistributionIncome.order_id).label('order_count')
        )

        # 添加过滤条件
        conditions = []

        # 用户ID筛选
        if 'user_id' in args and args['user_id']:
            conditions.append(DistributionIncome.user_id == args['user_id'])

        # 订单ID筛选
        if 'order_id' in args and args['order_id']:
            conditions.append(DistributionIncome.order_id == args['order_id'])

        # 状态筛选
        if 'status' in args and args['status'] is not None:
            conditions.append(DistributionIncome.status == args['status'])

        # 创建时间范围筛选
        if 'start_time' in args and args['start_time']:
            conditions.append(DistributionIncome.create_time >= args['start_time'])
        if 'end_time' in args and args['end_time']:
            conditions.append(DistributionIncome.create_time <= args['end_time'])

        # 将所有条件应用到查询
        if conditions:
            from sqlalchemy import and_
            query = query.filter(and_(*conditions))

        # 按状态分组并执行查询
        result = query.group_by(DistributionIncome.status).all()

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
