from flask.views import MethodView
from flask_jwt_extended import get_current_user

from backend.business.service.auth import auth_required
from backend.mini_core.schema.distribution import (
    DistributionQueryArgSchema, DistributionConfigQueryArgSchema, ReDistributionConfigSchema,
    DistributionGradeQueryArgSchema, ReDistributionGradeSchema, WXDistributionWxDataSchema,
    DistributionGradeUpdateQueryArgSchema, DistributionIncomeQueryArgSchema,
    DistributionLogQueryArgSchema
)
from backend.mini_core.service import (
    distribution_service, distribution_config_service,
    distribution_grade_service, distribution_grade_update_service,
    distribution_income_service, distribution_log_service,shop_user_service
)
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('wx_distribution', 'wx_distribution', url_prefix='/wx')


@blp.route('/distribution_wx')
class DistributionWXView(MethodView):
    """微信接口 分销中心初始界面"""
    decorators = [auth_required()]

    @blp.response()
    def get(self):
        """ 查看分销个人用户数据"""
        user = get_current_user()
        user_id = str(user.user_id)
        income = distribution_income_service.get_summary_by_user(user_id=user_id)
        income_d_m_a = distribution_income_service.get_income_d_m_a_summary(user_id=user_id)
        distribution_data = distribution_service.get({"user_id": user_id})["data"]

        from dataclasses import asdict


        if distribution_data:
            distribution_data = asdict(distribution_data)

            # 计算总佣金：wait_deposit_amount + frozen_amount + wait_amount 三者的和
            # 更安全的 null 值处理方式
            def safe_float(value):
                """安全地将值转换为 float，处理 None、空字符串等情况"""
                if value is None or value == '' :
                    return 0.0
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return 0.0

            wait_deposit_amount = safe_float(distribution_data.get("wait_deposit_amount"))
            frozen_amount = safe_float(distribution_data.get("frozen_amount"))
            wait_amount = safe_float(distribution_data.get("wait_amount"))

            total_amount = wait_deposit_amount + frozen_amount + wait_amount
            distribution_data["total_amount"] = round(float(total_amount), 2)

            user_father_invite_code = distribution_data.get("user_father_invite_code")
            if user_father_invite_code:
                shop_user_data = shop_user_service.find(invite_code=user_father_invite_code)
                if shop_user_data:
                    distribution_data["father_name"] = shop_user_data.nickname
        return dict(
            data=dict(
                income=income["data"],
                income_d_m_a=income_d_m_a["data"],
                distribution=distribution_data
            ),
            code=200
        )

@blp.route('/distribution')
class DistributionAPI(MethodView):
    """分销API"""
    @blp.arguments(DistributionQueryArgSchema, location='query')
    # @blp.response(ReDistributionSchemaList)
    def get(self, args: dict):
        """查看分销信息"""
        return distribution_service.data_list(args)

@blp.route('/distribution-config')
class DistributionConfigAPI(MethodView):
    """分销配置API"""

    @blp.arguments(DistributionConfigQueryArgSchema, location='query')
    @blp.response(ReDistributionConfigSchema)
    def get(self, args: dict):
        """查看分销配置"""
        return distribution_config_service.get(args)


@blp.route('/distribution-grade')
class DistributionGradeAPI(MethodView):
    """分销等级API"""

    @blp.arguments(DistributionGradeQueryArgSchema, location='query')
    @blp.response(ReDistributionGradeSchema)
    def get(self, args: dict):
        """查看分销等级"""
        return distribution_grade_service.get(args)


@blp.route('/distribution-grade-update')
class DistributionGradeUpdateAPI(MethodView):
    """分销等级更新API"""

    @blp.arguments(DistributionGradeUpdateQueryArgSchema, location='query')
    @blp.response(ReDistributionGradeSchema)
    def get(self, args: dict):
        """查看分销等级更新条件"""
        return distribution_grade_update_service.get(args)


@blp.route('/distribution_income')
class DistributionIncomeAPI(MethodView):
    """分销收入API"""
    decorators = [auth_required()]
    @blp.arguments(DistributionIncomeQueryArgSchema, location='query')
    @blp.response()
    def get(self, args: dict):
        """查看分销收入"""
        user = get_current_user()
        user_id = str(user.user_id)
        args["user_father_id"] =user_id
        return distribution_income_service.get(args)


@blp.route('/distribution-log')
class DistributionLogAPI(MethodView):
    """分销日志API"""
    decorators = [auth_required()]
    @blp.arguments(DistributionLogQueryArgSchema, location='query')
    def get(self, args: dict):
        """查看分销日志"""
        return distribution_log_service.get(args)


@blp.route('/distribution_members')
class DistributionMembersAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(DistributionQueryArgSchema, location="query")
    @blp.response()
    def get(self, args: dict):
        """ 分销成员的成员树状 """
        user = get_current_user()
        user_id = user.user_id
        args["user_id"] = user_id
        income = distribution_service.get_summary_build_tree(args)

        return income


@blp.route('/wx_distribution_data')
class DistributionRulesAPI(MethodView):
    decorators = [auth_required()]

    @blp.arguments(DistributionQueryArgSchema)
    @blp.response()
    def post(self, args: dict):
        return distribution_service.wx_get_distribution()
