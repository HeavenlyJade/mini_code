
from collections import defaultdict
from typing import List, Optional

from flask_jwt_extended import get_current_user

from backend.user import message
from backend.user.domain import Department
from backend.user.message import UserMessage
from backend.user.repository.department.base import DepartmentRepository
from kit.exceptions import ServiceBadRequest
from kit.service.base import CRUDService

__all__ = ['DepartmentService']


class DepartmentService(CRUDService[Department]):
    def __init__(self, repo: DepartmentRepository):
        super().__init__(repo)
        self._repo = repo

    @property
    def repo(self) -> DepartmentRepository:
        return self._repo

    def create(self, department: Department) -> Department:
        user = get_current_user()
        department.creator = user.username
        if department.parent_id:
            parent_department = self.get(department.parent_id)
            if not parent_department:
                raise ServiceBadRequest('选择的部门不存在')

            department.level = parent_department.level + 1
        return super().create(department)

    def delete(self, department_id: int) -> None:
        from backend.user.service import user_service
        departments = self.get_sub_departments(department_id)
        department_ids = [department.id for department in departments]
        users = user_service.repo.get_all(department_id=department_ids)
        for user, _ in users:
            if user.username == message.ADMIN_DEFAULT_USERNAME:
                raise ServiceBadRequest(UserMessage.ADMIN_DELETE_ERROR)
        user_ids = [user.id for user, _ in users]
        for user_id in user_ids:
            user_service.repo.delete_by({'id': user_id}, commit=False)
        for department_id in department_ids:
            self.repo.delete_by({'id': department_id}, commit=False)
        self.repo.commit()

    def update(self, department_id: int, department: Department) -> Optional[Department]:
        if department.parent_id == 0:
            department.level = 0
        else:
            department.level = self.get(department.parent_id).level + 1
        return super().update(department_id, department)

    def summary(self) -> list:
        departments = self.repo.find_all()
        level_department_map = defaultdict(list)
        summary = list()
        for department in departments:
            level_department_map[department.level].append(department)

        for department in level_department_map[0]:
            summary.append(
                dict(
                    id=department.id,
                    label=department.name,
                    value=department.name,
                    level=department.level,
                    children=self._get_children(department, level_department_map)
                )
            )
        return summary

    def _get_children(self, department: Department, level_department_map: dict) -> List[dict]:
        departments = list(filter(
            lambda x: x.parent_id == department.id,
            level_department_map[department.level + 1]
        ))
        return [
            dict(
                id=department.id,
                label=department.name,
                value=department.name,
                level=department.level,
                children=self._get_children(department, level_department_map)
            )
            for department in departments
        ]

    def get_sub_departments(self, department_id: int) -> List[Department]:
        def _traverse(parent_ids: List[int]) -> None:
            departments = self.repo.get_all(parent_id=parent_ids)
            departments = list(
                filter(lambda d: d.parent_id != d.id and d not in sub_departments, departments)
            )
            if not departments:
                return

            sub_departments.extend(departments)
            _traverse([department.id for department in departments])

        sub_departments = []
        parent_department = self.get(department_id)
        if not parent_department:
            return sub_departments

        sub_departments.append(parent_department)

        _traverse([department_id])
        return sub_departments
