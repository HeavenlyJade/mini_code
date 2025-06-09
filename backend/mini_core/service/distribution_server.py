from typing import Optional, Dict, Any
from dataclasses import asdict
from flask_jwt_extended import get_current_user
import datetime as dt
from backend.mini_core.domain.order.order import ShopOrder

from backend.mini_core.domain.distribution import (Distribution, DistributionConfig, DistributionGrade,
                                                   DistributionGradeUpdate, DistributionIncome, DistributionLog)
from backend.mini_core.repository.distribution.distribution_sqla import (DistributionSQLARepository,
                                                                         DistributionConfigSQLARepository,
                                                                         DistributionGradeSQLARepository,
                                                                         DistributionGradeUpdateSQLARepository,
                                                                         DistributionIncomeSQLARepository,
                                                                         DistributionLogSQLARepository)
from kit.service.base import CRUDService
from kit.util.datetime import datetime_str_to_ts, convert_timestamps_to_datetime, timestamp_to_datetime

__all__ = ['DistributionService', 'DistributionConfigService', 'DistributionGradeService',
           'DistributionGradeUpdateService', 'DistributionIncomeService', 'DistributionLogService']


class DistributionService(CRUDService[Distribution]):
    def __init__(self, repo: DistributionSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DistributionSQLARepository:
        return self._repo

    def get(self, args: dict) -> Dict[str, Any]:

        ser_args = {key: value for key, value in args.items()
                    if key in ["sn", "user_id"] and value is not None}
        if not ser_args:
            return dict(data={}, code=200)
        data = self._repo.find(**ser_args)

        if data:
            data = convert_timestamps_to_datetime(data)

        return {"data": data, "code": 200}

    def wx_find_update(self, args: dict) -> Dict[str, Any]:
        from backend.mini_core.service import shop_user_service
        user = get_current_user()
        user_id = str(user.user_id)
        user_father_invite_code = args["user_father_invite_code"]
        dis_data = self._repo.find(user_id=user_id)
        user_data = shop_user_service.find(invite_code=user_father_invite_code)
        if not user_data:
            return dict(data={}, code=400, message="上级邀请码的用户不存在")
        father_user_id = user_data.user_id
        dis_data.user_father_id = father_user_id
        dis_data.user_father_invite_code = user_father_invite_code
        re_data = self._repo.update(dis_data.id, dis_data)
        return dict(data=asdict(re_data), code=200)

    def data_list(self, args: dict) -> Dict[str, Any]:
        """
        获取分销用户列表数据，包含上级用户名称

        参数:
            args: 包含查询条件的字典，可能包含以下字段:
                - user_id/mobile/sn/real_name: 用户ID/手机号/编号/真实姓名
                - status: 状态(0-未审核, 1-已审核)
                - grade_id: 等级ID
                - page: 页码
                - size: 每页条数
                - start_time/end_time: 创建时间范围

        返回:
            包含上级用户名称的分销用户列表及总数
        """
        # 构建查询参数
        query_params = {"need_total_count": True}

        # 处理分页参数
        if "page" in args:
            query_params["page"] = args["page"]
        if "size" in args:
            query_params["size"] = args["size"]

        # 处理查询条件 - 精确匹配字段
        for key in ["sn", "user_id", "status", "grade_id"]:
            if key in args and args[key] is not None and args[key] != "":
                query_params[key] = args[key]

        # 处理模糊查询字段
        if "real_name" in args and args["real_name"]:
            query_params["real_name"] = args["real_name"]

        if "mobile" in args and args["mobile"]:
            query_params["mobile"] = args["mobile"]

        # 处理时间范围查询
        if "start_time" in args and "end_time" in args and args["start_time"] and args["end_time"]:
            query_params["create_time"] = [args["start_time"], args["end_time"]]

        # 执行带有上级用户信息的查询
        data, total = self._repo.list_with_parent_info(**query_params)
        # 返回结果
        return {"data": data, "total": total, "code": 200}

    def get_summary_build_tree(self, args) -> Dict[str, Any]:
        """
        构建分销成员的树形结构，整合用户信息和分销信息

        Args:
            args: 包含查询参数的字典

        Returns:
            包含树形结构数据的字典
        """
        # 获取数据
        user_id = args['user_id']

        # 从数据库获取层级数据
        sql_data = self._repo.get_summary_tree(args)

        # 转换为树状结构数据格式 (适合前端渲染)
        def convert_to_tree_format(data, parent_id, current_level=1):
            """
            递归构建树形结构

            Args:
                data: 所有用户数据列表
                parent_id: 父级用户ID
                current_level: 当前层级

            Returns:
                树形节点列表
            """
            tree_nodes = []
            # 筛选出当前父级下的直接子级
            children = [item for item in data if str(item['user_father_id']) == str(parent_id)]

            for child in children:
                child_user_id = str(child['user_id'])

                # 构建节点信息，整合分销信息和用户信息
                node = {
                    'id': child_user_id,
                    'distribution_id': child.get('distribution_id'),
                    'name': child.get('real_name') or child.get('nickname') or child.get('username', '未知用户'),
                    'real_name': child.get('real_name'),
                    'nickname': child.get('nickname'),
                    'username': child.get('username'),
                    'mobile': child.get('mobile'),
                    'avatar': child.get('avatar'),
                    'remark': child.get('remark'),
                    'status': child.get('status'),
                    'user_status': child.get('user_status'),
                    'grade_id': child.get('grade_id'),
                    'identity': child.get('identity'),
                    'level': current_level,
                    'sn': child.get('sn'),
                    'last_login_time': child.get('last_login_time'),
                    'audit_time': child.get('audit_time'),
                    'create_time': child.get('distribution_create_time'),
                    'isLeaf': True,  # 默认为叶子节点，后续会更新
                    'children': convert_to_tree_format(data, child_user_id, current_level + 1)
                }

                # 如果有子节点，则不是叶子节点
                if node['children']:
                    node['isLeaf'] = False

                tree_nodes.append(node)

            return tree_nodes

        # 构建树结构数据
        tree_data = {
            'id': str(user_id),
            'name': '分销成员',
            'level': 0,
            'isLeaf': False,
            'children': convert_to_tree_format(sql_data, user_id)
        }

        # 统计信息
        total_members = len(sql_data)
        active_members = len([item for item in sql_data if item.get('status') == 1])

        # 计算各层级数量
        level_stats = {}
        for item in sql_data:
            level = item.get('level', 1)
            level_stats[level] = level_stats.get(level, 0) + 1

        return dict(
            code=200,
            data=tree_data,
            statistics={
                'total_members': total_members,
                'active_members': active_members,
                'level_stats': level_stats
            }
        )

    def get_by_user_id(self, user_id: str) -> Optional[Any]:
        return self._repo.find(user_id=user_id)

    def update(self, user_id, distribution: Distribution) -> Dict[str, Any]:
        user_data = self.get_by_user_id(user_id)
        if not user_data:
            return dict(message="用户不存在", code=400)

        has_updates = False
        for field, value in distribution.__dict__.items():
            if value is not None:
                setattr(user_data, field, value)
                has_updates = True
        if has_updates:
            result = self.repo.update(user_data.id, user_data)
            return dict(data=result, code=200)
        else:
            return dict(message="无需更新的数据", code=400)

    def create(self, distribution: Distribution) -> Dict[str, Any]:
        result = self._repo.create(distribution)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        result = super().delete(id)
        return dict(data=result, code=200)

    def audit(self, id: int, status: int) -> Dict[str, Any]:
        distribution = self._repo.get(id)
        if not distribution:
            return dict(data=None, code=404, message="分销记录不存在")

        distribution.status = status
        result = self._repo.update(distribution)
        return dict(data=result, code=200)

    def get_distribution(self, dis_id: int):
        distribution_user_data = self._repo.get_by_id(dis_id)
        return asdict(distribution_user_data)

    def wx_get_distribution(self, ):
        from backend.mini_core.service import distribution_grade_service, distribution_config_service
        current_user = get_current_user()
        current_user_openid = current_user.openid
        distribution_user_data = self._repo.find(sn=current_user_openid)
        dis_data = distribution_grade_service.grader_data_list({})
        grade_data = dis_data.get("data")
        config_data, _ = distribution_config_service.config_data_list()
        distribution_user_data = asdict(distribution_user_data)
        config_data = [dict(content=i.content, title=i.title) for i in config_data]
        grade_data = [asdict(i) for i in grade_data]
        return dict(config_data=config_data, grade_data=grade_data, distribution_user_data=distribution_user_data)

    def get_user_team_data(self, args):
        data, total = self._repo.list(**args)
        re_team = []
        for item in data:
            real_name = item.real_name
            real_name = real_name[0] + '*' * (len(real_name) - 2) + real_name[-1]
            re_dic = dict(real_name=real_name, lv_id=item.lv_id, user_id=item.user_id)
            re_team.append(re_dic)
        return dict(data=re_team, total=total, code=200)


class DistributionConfigService(CRUDService[DistributionConfig]):
    def __init__(self, repo: DistributionConfigSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DistributionConfigSQLARepository:
        return self._repo

    def config_data_list(self, **kwargs):
        data = self._repo.list()
        return data

    def get(self, args: dict) -> Dict[str, Any]:
        key = args.get("key")
        data = self._repo.find(key=key)
        return dict(data=data, code=200)

    def get_by_key(self, key: str) -> Optional[DistributionConfig]:
        return self._repo.find(key=key)

    def update(self, id: int, config: DistributionConfig) -> Dict[str, Any]:
        result = self._repo.update(id, config)
        return dict(data=result, code=200)

    def create(self, config: DistributionConfig) -> Dict[str, Any]:
        result = super().create(config)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        result = super().delete(id)
        return dict(data=result, code=200)


class DistributionGradeService(CRUDService[DistributionGrade]):
    def __init__(self, repo: DistributionGradeSQLARepository,
                 grade_update_repo: DistributionGradeUpdateSQLARepository):
        super().__init__(repo)
        self._repo = repo
        self._grade_update_repo = grade_update_repo

    @property
    def repo(self) -> DistributionGradeSQLARepository:
        return self._repo

    def find_all_dis_config(self, args: dict) -> Dict:
        data = self._repo.find_all(**args)
        return {item.id: item.name for item in data}

    def grader_data_list(self, args: dict):
        data, total = self._repo.list(**args)
        return dict(data=data, total=total, code=200)

    def get(self, args: dict) -> Dict[str, Any]:
        name = args.get("name")
        data = self._repo.find(name=name)
        return dict(data=data, code=200)

    def update(self, id: int, grade: DistributionGrade) -> Dict[str, Any]:
        result = self._repo.update(id, grade)
        return dict(data=result, code=200)

    def create(self, grade: DistributionGrade) -> Dict[str, Any]:
        result = self._repo.create(grade)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        # 先删除关联的条件
        # self._grade_update_repo.delete_by(grade_id=id)
        result = self._repo.delete(id)
        return dict(data=result, code=200)


class DistributionGradeUpdateService(CRUDService[DistributionGradeUpdate]):
    def __init__(self, repo: DistributionGradeUpdateSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DistributionGradeUpdateSQLARepository:
        return self._repo

    def get(self, args: dict) -> Dict[str, Any]:
        grade_id = args.get("grade_id")
        key = args.get("key")
        if key:
            data = self._repo.find(grade_id=grade_id, key=key)
        else:
            data = self._repo.list(grade_id=grade_id)
        return dict(data=data, code=200)

    def update(self, id: int, condition: DistributionGradeUpdate) -> Dict[str, Any]:
        result = super().update(id, condition)
        return dict(data=result, code=200)

    def create(self, condition: DistributionGradeUpdate) -> Dict[str, Any]:
        result = super().create(condition)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        result = super().delete(id)
        return dict(data=result, code=200)

    def update_or_create(self, grade_id: int, key: str, value: float) -> Dict[str, Any]:
        condition = self._repo.find(grade_id=grade_id, key=key)
        if condition:
            condition.value = value
            result = self._repo.update(condition)
        else:
            condition = DistributionGradeUpdate()
            condition.grade_id = grade_id
            condition.key = key
            condition.value = value
            result = self._repo.create(condition)
        return dict(data=result, code=200)


class DistributionIncomeService(CRUDService[DistributionIncome]):
    def __init__(self, repo: DistributionIncomeSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DistributionIncomeSQLARepository:
        return self._repo

    def get(self, args: dict) -> Dict[str, Any]:
        user_father_id = args.get("user_father_id")
        order_id = args.get("order_id")
        status = args.get("status")
        end_date = args.get("end_date")
        start_date = args.get("start_date")
        query_args = {}
        if user_father_id:
            query_args["user_father_id"] = user_father_id
        if order_id:
            query_args["order_id"] = order_id
        if status is not None and int(status) != -1:
            query_args["status"] = status
        if end_date and start_date:
            query_args["create_time"] =[start_date, end_date]

        query_args["need_total_count"] = args.get("need_total_count")
        query_args["page"] = args.get("page")
        query_args["size"] = args.get("size")
        query_args["ordering"] =["-create_time"]
        data, total = self._repo.list(**query_args)
        re_data = []
        for i in data:
            re_data.append(asdict(i))
        return dict(data=re_data, code=200, total=total)

    def get_summary_by_user(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户分销收入汇总信息

        参数:
            user_id: 用户ID

        返回:
            包含汇总数据和状态码的字典
        """
        if not user_id:
            return dict(data={}, code=400)
        args = dict(user_id=user_id)
        incomes = self._repo.get_money_sum_by_status(args)

        status_money = {3: 0, 1: 0, 2: 0}  # 0:待结算, 1:已结算, 2:已冻结
        for income in incomes:
            if income.status in status_money:
                status_money[income.status] = income.total_money
        # 计算总金额
        total_money = sum(income.total_money for income in incomes)
        result = {
            "user_id": user_id,
            "total_money": total_money,
            "pending_money": status_money[3],
            "settled_money": status_money[1],
            "frozen_money": status_money[2]
        }
        return {"data": result, "code": 200}

    def get_income_d_m_a_summary(self, user_id: int) -> Dict[str, Any]:
        if not user_id:
            return dict(data=dict(today_income=0, month_income=0, total_income=0), code=400)
        result = self._repo.get_income_summary(user_id=user_id)
        return dict(data=result, code=200)

    def get_income_statistics(self, args: dict = None) -> dict:
        """
        获取收入统计数据，返回格式化的字典结果

        参数:
            args: 包含查询条件的字典，可以包含以下键:
                - user_id: 用户ID
                - order_id: 订单ID
                - status: 状态码
                - start_time: 创建时间开始范围
                - end_time: 创建时间结束范围

        返回:
            包含各状态收入统计的字典
        """
        # 确保args是一个字典
        args = args or {}

        # 获取按状态分组的统计数据
        stats = self._repo.get_money_sum_by_status(args)

        # 初始化结果字典，确保即使没有数据也有默认值
        result = {
            "total_income": 0,
            "pending_income": 0,  # 状态 0：待结算
            "settled_income": 0,  # 状态 1：已结算
            "frozen_income": 0,  # 状态 2：已冻结
            "total_order_count": 0,
            "pending_order_count": 0,
            "settled_order_count": 0,
            "frozen_order_count": 0
        }

        # 计算总收入和总订单数
        total_income = 0
        total_orders = 0

        for stat in stats:
            status_code = stat[0]
            amount = float(stat[1]) if stat[1] else 0
            order_count = int(stat[2]) if stat[2] else 0

            total_income += amount
            total_orders += order_count

            # 根据状态码填充相应的字段
            if status_code == 3:
                result["pending_income"] = amount
                result["pending_order_count"] = order_count
            elif status_code == 1:
                result["settled_income"] = amount
                result["settled_order_count"] = order_count
            elif status_code == 2:
                result["frozen_income"] = amount
                result["frozen_order_count"] = order_count

        result["total_income"] = total_income
        result["total_order_count"] = total_orders
        return result

    def update(self, id: int, income: DistributionIncome) -> Dict[str, Any]:
        result = self._repo.update(id, income)
        return dict(data=result, code=200)

    def create(self, income: DistributionIncome) -> Dict[str, Any]:
        result = self._repo.create(income)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        result = self._repo.delete(id)
        return dict(data=result, code=200)

    def update_status(self, id: int, status: int) -> Dict[str, Any]:
        income = self._repo.get(id)
        if not income:
            return dict(data=None, code=404, message="收入记录不存在")

        income.status = status
        result = self._repo.update(income)
        return dict(data=result, code=200)


class DistributionLogService(CRUDService[DistributionLog]):
    def __init__(self, repo: DistributionLogSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DistributionLogSQLARepository:
        return self._repo

    def get(self, args: dict) -> Dict[str, Any]:
        distribution_id = args.get("distribution_id")
        change_object = args.get("change_object")
        change_type = args.get("change_type")

        query_args = {}
        if distribution_id:
            query_args["distribution_id"] = distribution_id
        if change_object:
            query_args["change_object"] = change_object
        if change_type:
            query_args["change_type"] = change_type

        data = self._repo.list(**query_args)
        return dict(data=data, code=200)

    def update(self, id: int, log: DistributionLog) -> Dict[str, Any]:
        result = super().update(id, log)
        return dict(data=result, code=200)

    def create(self, log: DistributionLog) -> Dict[str, Any]:
        result = super().create(log)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        result = super().delete(id)
        return dict(data=result, code=200)

    def record_change(self, distribution_id: int, change_object: str,
                      change_type: str, action: str, before_amount: float,
                      left_amount: float, source_id: int = None,
                      source_sn: str = None, extra: str = None,
                      admin_id: int = None) -> DistributionLog:
        log = DistributionLog()
        log.distribution_id = distribution_id
        log.change_object = change_object
        log.change_type = change_type
        log.action = action
        log.before_amount = before_amount
        log.left_amount = left_amount
        log.source_id = source_id
        log.source_sn = source_sn
        log.extra = extra
        log.admin_id = admin_id

        result = self._repo.create(log)
        return result
