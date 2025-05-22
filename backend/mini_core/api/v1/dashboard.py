from flask.views import MethodView
from backend.business.service.auth import auth_required
from backend.mini_core.service import dashboard_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('dashboard', 'dashboard', url_prefix='/dashboard')


@blp.route('/overview')
class DashboardOverviewAPI(MethodView):
    """仪表盘总览API"""
    # decorators = [auth_required()]

    def get(self):
        """获取仪表盘总览数据"""
        return dashboard_service.get_dashboard_data()
