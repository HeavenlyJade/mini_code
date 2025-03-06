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
        sn = args.get("sn")
        if sn:
            data = self._repo.find(sn=sn)
        else:
            user_id = args.get("user_id")
            data = self._repo.find(user_id=user_id)
        return dict(data=data, code=200)

    def get_by_user_id(self, user_id: int) -> Optional[Distribution]:
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

        query_args = {}
        if user_id:
            query_args["user_id"] = user_id
        if order_id:
            query_args["order_id"] = order_id
        if status is not None:
            query_args["status"] = status

        data = self._repo.list(**query_args)
        return dict(data=data, code=200)

    def get_summary_by_user(self, user_id: int) -> Dict[str, Any]:
        incomes = self._repo.list(user_id=user_id)

        total_money = sum(income.money for income in incomes)
        pending_money = sum(income.money for income in incomes if income.status == 0)
        settled_money = sum(income.money for income in incomes if income.status == 2)
        frozen_money = sum(income.money for income in incomes if income.status == 3)

        result = {
            "user_id": user_id,
            "total_money": total_money,
            "pending_money": pending_money,
            "settled_money": settled_money,
            "frozen_money": frozen_money
        }

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
