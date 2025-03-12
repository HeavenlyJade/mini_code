from flask.views import MethodView

from backend.mini_core.schema.distribution import (
    DistributionQueryArgSchema, ReDistributionSchema,
    DistributionConfigQueryArgSchema, ReDistributionConfigSchema,
    DistributionGradeQueryArgSchema, ReDistributionGradeSchema,
    DistributionGradeUpdateQueryArgSchema, DistributionIncomeQueryArgSchema,
    ReDistributionIncomeSchema, DistributionLogQueryArgSchema,
    Distribution, DistributionConfig, DistributionGrade,
    DistributionGradeUpdate, DistributionIncome, DistributionLog
)
from backend.mini_core.service import (
    distribution_service, distribution_config_service,
    distribution_grade_service, distribution_grade_update_service,
    distribution_income_service, distribution_log_service
)
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('distribution', 'distribution', url_prefix='/')


@blp.route('/distribution_wx')
class DistributionWXView(MethodView):
    """微信接口 分销中心初始界面"""

    @blp.arguments(DistributionQueryArgSchema, location='query')
    @blp.response()
    def get(self, args: dict):
        """查看分销集体信息"""
        print(args)
        income = distribution_income_service.get_summary_by_user(user_id=args.get("user_id"))
        income_d_m_a = distribution_income_service.get_income_d_m_a_summary(user_id=args.get("user_id"))
        distribution = distribution_service.get(args)["data"]
        return dict(data=dict(income=income, income_d_m_a=income_d_m_a, distribution=distribution), code=200)


@blp.route('/distribution')
class DistributionAPI(MethodView):
    """分销API"""

    @blp.arguments(DistributionQueryArgSchema, location='query')
    @blp.response(ReDistributionSchema)
    def get(self, args: dict):
        """查看分销信息"""
        return distribution_service.get(args)

    @blp.arguments(Distribution)
    @blp.response(ReDistributionSchema)
    def post(self, distribution):
        """新增分销信息"""
        return distribution_service.update(distribution["user_id"], distribution)


@blp.route('/distribution-config')
class DistributionConfigAPI(MethodView):
    """分销配置API"""

    @blp.arguments(DistributionConfigQueryArgSchema, location='query')
    @blp.response(ReDistributionConfigSchema)
    def get(self, args: dict):
        """查看分销配置"""
        return distribution_config_service.get(args)

    @blp.arguments(DistributionConfig)
    @blp.response(ReDistributionConfigSchema)
    def post(self, config):
        """更新分销配置"""
        return distribution_config_service.update(config["key"], config)


@blp.route('/distribution-grade')
class DistributionGradeAPI(MethodView):
    """分销等级API"""

    @blp.arguments(DistributionGradeQueryArgSchema, location='query')
    @blp.response(ReDistributionGradeSchema)
    def get(self, args: dict):
        """查看分销等级"""
        return distribution_grade_service.get(args)

    @blp.arguments(DistributionGrade)
    @blp.response(ReDistributionGradeSchema)
    def post(self, grade):
        """更新分销等级"""
        return distribution_grade_service.update(grade["id"], grade)


@blp.route('/distribution-grade-update')
class DistributionGradeUpdateAPI(MethodView):
    """分销等级更新API"""

    @blp.arguments(DistributionGradeUpdateQueryArgSchema, location='query')
    @blp.response(ReDistributionGradeSchema)
    def get(self, args: dict):
        """查看分销等级更新条件"""
        return distribution_grade_update_service.get(args)

    @blp.arguments(DistributionGradeUpdate)
    @blp.response(ReDistributionGradeSchema)
    def post(self, update):
        """更新分销等级条件"""
        return distribution_grade_update_service.update(update["id"], update)


@blp.route('/distribution_income')
class DistributionIncomeAPI(MethodView):
    """分销收入API"""

    @blp.arguments(DistributionIncomeQueryArgSchema, location='query')
    @blp.response()
    def get(self, args: dict):
        """查看分销收入"""
        return distribution_income_service.get(args)

    @blp.arguments(DistributionIncome)
    @blp.response()
    def post(self, income):
        """更新分销收入"""
        return distribution_income_service.update(income["id"], income)


@blp.route('/distribution-log')
class DistributionLogAPI(MethodView):
    """分销日志API"""

    @blp.arguments(DistributionLogQueryArgSchema, location='query')
    def get(self, args: dict):
        """查看分销日志"""
        return distribution_log_service.get(args)

    @blp.arguments(DistributionLog)
    def post(self, log):
        """添加分销日志"""
        return distribution_log_service.update(log["id"], log)
