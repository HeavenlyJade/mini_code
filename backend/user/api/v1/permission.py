from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.user.domain.permission import Permission
from backend.user.schema.permission import (
    PermissionCreateSchema,
    PermissionListSchema,
    PermissionQueryArgSchema,
    PermissionSchema,
    PermissionTreeSchema,
    PermissionUpdateSchema,
)
from backend.user.service import  permission_service
from kit.schema.base import RespSchema
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('permissions', 'permissions', url_prefix='/')


@blp.route('/')
class PermissionAPI(MethodView):
    """权限管理API"""

    decorators = [jwt_required()]

    @blp.arguments(PermissionQueryArgSchema, location='query')
    @blp.response(PermissionListSchema)
    def get(self, args: dict):
        """权限管理 查看权限列表"""
        return permission_service.list(args)

    @blp.arguments(PermissionCreateSchema)
    @blp.response(PermissionSchema)
    def post(self, permission: Permission):
        """权限管理 创建权限"""
        return permission_service.create(permission)


@blp.route('/<int:permission_id>')
class PermissionByIDAPI(MethodView):
    """单个权限管理API"""

    decorators = [jwt_required()]

    @blp.response(PermissionSchema)
    def get(self, permission_id: int):
        """权限管理 查看权限详情"""
        return permission_service.get(permission_id)

    @blp.arguments(PermissionUpdateSchema)
    @blp.response(PermissionSchema)
    def put(self, permission: Permission, permission_id: int):
        """权限管理 编辑权限"""
        return permission_service.update(permission_id, permission)

    @blp.response(RespSchema)
    def delete(self, permission_id: int):
        """权限管理 删除权限"""
        permission_service.delete(permission_id)
        return {'code': 200, 'message': '删除成功'}


@blp.route('/tree')
class PermissionTreeAPI(MethodView):
    """权限树API"""

    decorators = [jwt_required()]

    @blp.response(PermissionTreeSchema)
    def get(self):
        """权限管理 获取权限树结构"""
        tree = permission_service.get_permission_tree()
        return {'items': tree}


@blp.route('/menus')
class MenuPermissionsAPI(MethodView):
    """菜单权限API"""

    decorators = [jwt_required()]

    @blp.response(PermissionTreeSchema)
    def get(self):
        """权限管理 获取菜单权限树结构"""
        menus = permission_service.get_menu_permissions()
        return {'items': menus}


@blp.route('/user/menus')
class UserMenusAPI(MethodView):
    """用户菜单API"""

    decorators = [jwt_required()]

    @blp.response(PermissionTreeSchema)
    def get(self):
        """权限管理 获取当前用户的菜单权限"""
        username = get_jwt_identity()
        menus = permission_service.get_user_menus(username)
        return {'items': menus}
