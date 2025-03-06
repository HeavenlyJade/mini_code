from flask.views import MethodView

from backend.business.service.auth import auth_required
from backend.user.domain import Department
from backend.user.schema.department import (
    DepartmentCreateSchema,
    DepartmentSchema,
    DepartmentUpdateSchema,
    DepartmentPatchSchema,
    DepartmentQueryArgSchema,
    DepartmentListSchema,
)
from backend.user.service import department_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('departments', 'departments', url_prefix='/')


@blp.route('/')
class DepartmentAPI(MethodView):
    """部门管理API"""

    decorators = [auth_required()]

    @blp.arguments(DepartmentQueryArgSchema, location='query')
    @blp.response(DepartmentListSchema)
    def get(self, args: dict):
        """部门管理 查看部门列表"""
        return department_service.list(args)

    @blp.arguments(DepartmentCreateSchema)
    @blp.response(DepartmentSchema)
    def post(self, department: Department):
        """部门管理 创建部门"""
        return department_service.create(department)


@blp.route('/<int:department_id>')
class DepartmentByIDAPI(MethodView):
    decorators = [auth_required()]

    @blp.response(DepartmentSchema)
    def get(self, department_id: int):
        """部门管理 查看部门详情"""
        return department_service.get(department_id)

    @blp.arguments(DepartmentUpdateSchema)
    @blp.response(DepartmentSchema)
    def put(self, department: Department, department_id: int):
        """部门管理 编辑部门"""
        return department_service.update(department_id, department)

    @blp.arguments(DepartmentPatchSchema)
    @blp.response(DepartmentSchema)
    def patch(self, department: Department, department_id: int):
        """部门管理 更新部门"""
        return department_service.update(department_id, department)

    @blp.response(RespSchema)
    def delete(self, department_id: int):
        """部门管理 删除部门信息"""
        return department_service.delete(department_id)


@blp.route('/summary')
class DepartmentSummaryAPI(MethodView):

    @blp.response()
    def get(self):
        return department_service.summary()
