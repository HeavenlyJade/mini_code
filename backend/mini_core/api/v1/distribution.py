from flask.views import MethodView
from flask_jwt_extended import get_current_user

from backend.business.service.auth import auth_required
from backend.mini_core.schema.distribution import (
    DistributionQueryArgSchema, ReDistributionSchema, DistributionConfigQueryArgSchema, DistributionGradeQueryArgSchema,
    ReDistributionGradeSchema, DistributionConfigSchema,
    DistributionGradeUpdateQueryArgSchema, DistributionIncomeQueryArgSchema,
    DistributionLogQueryArgSchema, ReDistributionGradeListSchema, DistributionGradeSchema, Distribution,
    ReDistributionConfigDataSchema, ReDistributionConfigSchema,
    DistributionGradeUpdate, DistributionIncome, DistributionLog
)
from backend.mini_core.service import (
    distribution_service, distribution_config_service,
    distribution_grade_service, distribution_grade_update_service,
    distribution_income_service, distribution_log_service
)
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('distribution', 'distribution', url_prefix='/')


@blp.route('/distribution_web')
class DistributionWXView(MethodView):
    """ 分销数据初始化"""
    decorators = [auth_required()]

    @blp.arguments(DistributionQueryArgSchema, location='query')
    @blp.response()
    def get(self, args: dict):
        """查询分销页面的数据"""
        income = distribution_income_service.get_income_statistics(args)
        return dict(data=dict(income=income, ), code=200)


@blp.route('/distribution')
class DistributionAPI(MethodView):
    """分销API"""
    decorators = [auth_required()]

    @blp.arguments(DistributionQueryArgSchema, location='query')
    # @blp.response(ReDistributionSchemaList)
    def get(self, args: dict):
        """查看分销信息"""
        return distribution_service.data_list(args)

    @blp.arguments(Distribution)
    @blp.response(ReDistributionSchema)
    def post(self, distribution):
        """新增分销信息"""
        return distribution_service.update(distribution["user_id"], distribution)


@blp.route('/distribution/<int:dis_id>')
class DistributionUserAPI(MethodView):
    """分销API"""
    decorators = [auth_required()]

    @blp.response()
    def get(self, dis_id):
        """查看分销信息"""
        dis_user_data = distribution_service.get_distribution(dis_id)
        income_dict = dict(user_id=dis_user_data["user_id"])
        income = distribution_income_service.get_income_statistics(income_dict)
        re_data = dict(data=dis_user_data, income=income, code=200)
        return re_data


@blp.route('/distribution-config')
class DistributionConfigAPI(MethodView):
    """分销配置API"""
    decorators = [auth_required()]

    @blp.arguments(DistributionConfigQueryArgSchema, location='query')
    @blp.response(ReDistributionConfigSchema)
    def get(self, args: dict):
        """查看分销配置"""

        data, total = distribution_config_service.config_data_list(**args)
        return dict(total=total, data=data, code=200)

    @blp.arguments(DistributionConfigSchema)
    @blp.response(ReDistributionConfigDataSchema)
    def post(self, args):
        return distribution_config_service.create(args)


@blp.route('/distribution-config/<int:data_id>')
class DistributionGradePatchAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(DistributionConfigSchema)
    @blp.response(ReDistributionConfigDataSchema)
    def put(self, config, data_id):
        """更新分销配置"""
        return distribution_config_service.update(data_id, config)

    @blp.response(ReDistributionConfigDataSchema)
    def delete(self, data_id):
        return distribution_config_service.delete(data_id)


@blp.route('/distribution-grade-list')
class DistributionConfigAPI(MethodView):
    decorators = [auth_required()]

    @blp.response()
    def get(self, ):
        return distribution_grade_service.find_all_dis_config({})


@blp.route('/distribution-grade')
class DistributionGradeAPI(MethodView):
    """分销等级API"""
    decorators = [auth_required()]

    @blp.arguments(DistributionGradeQueryArgSchema, location='query')
    @blp.response(ReDistributionGradeListSchema)
    def get(self, args: dict):
        """查看分销等级"""
        return distribution_grade_service.grader_data_list(args)

    @blp.arguments(DistributionGradeSchema)
    @blp.response(ReDistributionGradeSchema)
    def post(self, grade):
        """更新分销等级"""
        return distribution_grade_service.create(grade)


@blp.route('/distribution-grade/<int:data_id>')
class DistributionGradeAPI(MethodView):
    """ 分析修改和删除API"""
    decorators = [auth_required()]

    @blp.arguments(DistributionGradeSchema)
    @blp.response(ReDistributionGradeSchema)
    def put(self, args, data_id):
        """修改分销等级"""
        return distribution_grade_service.update(data_id, args)

    @blp.response()
    def delete(self, data_id):
        """删除分销等级配置"""
        return distribution_grade_service.delete(data_id)


@blp.route('/distribution-grade-update')
class DistributionGradeUpdateAPI(MethodView):
    """分销等级更新API"""
    decorators = [auth_required()]

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
    decorators = [auth_required()]

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
    decorators = [auth_required()]

    @blp.arguments(DistributionLogQueryArgSchema, location='query')
    def get(self, args: dict):
        """查看分销日志"""
        return distribution_log_service.get(args)

    @blp.arguments(DistributionLog)
    def post(self, log):
        """添加分销日志"""
        return distribution_log_service.update(log["id"], log)


@blp.route('/distribution_members')
class DistributionMembersAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(DistributionQueryArgSchema, location="query")
    @blp.response()
    def get(self, args: dict):
        """ 分销成员的成员树状 """
        income = distribution_service.get_summary_build_tree(args)

        return income

    def post(self):
        pass
