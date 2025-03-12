from typing import Optional, List, Dict, Any

from kit.service.base import CRUDService
from backend.mini_core.domain.distribution import (Distribution, DistributionConfig, DistributionGrade,
                                                   DistributionGradeUpdate, DistributionIncome, DistributionLog)

from backend.mini_core.repository.distribution.distribution_sqla import (DistributionSQLARepository,
                                                                         DistributionConfigSQLARepository,
                                                                         DistributionGradeSQLARepository,
                                                                         DistributionGradeUpdateSQLARepository,
                                                                         DistributionIncomeSQLARepository,
                                                                         DistributionLogSQLARepository)
from kit.util.datetime import datetime_str_to_ts,convert_timestamps_to_datetime

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
            return dict(data={},code=200)
        data = self._repo.find(**ser_args)
        if data:
            data = convert_timestamps_to_datetime(data)

        return {"data": data, "code": 200}

    def get_by_user_id(self, user_id: int) -> Optional[Any]:
        return self._repo.find(user_id=user_id)

    def update(self, id: int, distribution: Distribution) -> Dict[str, Any]:
        result = super().update(id, distribution)
        return dict(data=result, code=200)

    def create(self, distribution: Distribution) -> Dict[str, Any]:
        result = super().create(distribution)
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


class DistributionConfigService(CRUDService[DistributionConfig]):
    def __init__(self, repo: DistributionConfigSQLARepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DistributionConfigSQLARepository:
        return self._repo

    def get(self, args: dict) -> Dict[str, Any]:
        key = args.get("key")
        data = self._repo.find(key=key)
        return dict(data=data, code=200)

    def get_by_key(self, key: str) -> Optional[DistributionConfig]:
        return self._repo.find(key=key)

    def update(self, id: int, config: DistributionConfig) -> Dict[str, Any]:
        result = super().update(id, config)
        return dict(data=result, code=200)

    def create(self, config: DistributionConfig) -> Dict[str, Any]:
        result = super().create(config)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        result = super().delete(id)
        return dict(data=result, code=200)

    def get_value_by_key(self, key: str) -> str:
        config = self._repo.find(key=key)
        return config.value if config else ""


class DistributionGradeService(CRUDService[DistributionGrade]):
    def __init__(self, repo: DistributionGradeSQLARepository,
                 grade_update_repo: DistributionGradeUpdateSQLARepository):
        super().__init__(repo)
        self._repo = repo
        self._grade_update_repo = grade_update_repo

    @property
    def repo(self) -> DistributionGradeSQLARepository:
        return self._repo

    def get(self, args: dict) -> Dict[str, Any]:
        name = args.get("name")
        data = self._repo.find(name=name)
        return dict(data=data, code=200)

    def get_with_conditions(self, id: int) -> Dict[str, Any]:
        grade = self._repo.get(id)
        if not grade:
            return dict(data=None, code=404, message="等级不存在")

        conditions = self._grade_update_repo.list(grade_id=id)
        result = {
            "id": grade.id,
            "name": grade.name,
            "weight": grade.weight,
            "self_ratio": grade.self_ratio,
            "first_ratio": grade.first_ratio,
            "second_ratio": grade.second_ratio,
            "remark": grade.remark,
            "update_relation": grade.update_relation,
            "conditions": conditions
        }
        return dict(data=result, code=200)

    def update(self, id: int, grade: DistributionGrade) -> Dict[str, Any]:
        result = super().update(id, grade)
        return dict(data=result, code=200)

    def create(self, grade: DistributionGrade) -> Dict[str, Any]:
        result = super().create(grade)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        # 先删除关联的条件
        self._grade_update_repo.delete_by(grade_id=id)
        result = super().delete(id)
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
        user_id = args.get("user_id")
        order_id = args.get("order_id")
        status = args.get("status")
        end_date = args.get("end_date")
        start_date = args.get("start_date")

        query_args = {}
        if user_id:
            query_args["user_id"] = user_id
        if order_id:
            query_args["order_id"] = order_id
        if status is not None and int(status) !=-1 :
            query_args["status"] = status
        if end_date and start_date:
            start_date = datetime_str_to_ts(start_date)
            end_date = datetime_str_to_ts(end_date)
            if status in [0,2]:
                query_args["create_time"] = [start_date, end_date]
            elif start_date ==1:
                query_args["settlement_time"] = [start_date, end_date]
        data, total = self._repo.list(**query_args)
        for i in data:
            convert_timestamps_to_datetime(i)
        return dict(data=data, code=200,total=total)

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
        incomes = self._repo.get_money_sum_by_status(user_id)

        status_money = {0: 0, 1: 0, 2: 0}  # 0:待结算, 1:已结算, 2:已冻结
        for income in incomes:
            if income.status in status_money:
                status_money[income.status] = income.total_money
        # 计算总金额
        total_money = sum(income.total_money for income in incomes)
        result = {
            "user_id": user_id,
            "total_money": total_money,
            "pending_money": status_money[0],
            "settled_money": status_money[1],
            "frozen_money": status_money[2]
        }
        return {"data": result, "code": 200}

    def get_income_d_m_a_summary(self,user_id: int) -> Dict[str, Any]:
        if not user_id:
            return dict(data=dict(today_income=0,month_income=0,total_income=0), code=400)
        result = self._repo.get_income_summary(user_id=user_id)
        return dict(data=result, code=200)
    def update(self, id: int, income: DistributionIncome) -> Dict[str, Any]:
        result = super().update(id, income)
        return dict(data=result, code=200)

    def create(self, income: DistributionIncome) -> Dict[str, Any]:
        result = super().create(income)
        return dict(data=result, code=200)

    def delete(self, id: int) -> Dict[str, Any]:
        result = super().delete(id)
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
