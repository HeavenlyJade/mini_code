# -*- coding: utf-8 -*-
# author zyy
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from backend.license_management.schema.li import LiQueryArgSchemaRequests, LiSchemaResponse, LiDlSchemaResponse, \
    LiUploadSchemaResponse
from backend.license_management.service import li_service
from kit.util.blueprint import APIBlueprint

li_blp = APIBlueprint('license', 'license', url_prefix='/license')


@li_blp.route('/')
class LicenseAPI(MethodView):
    """LicenseAPI"""
    @li_blp.arguments(LiQueryArgSchemaRequests, location='query')
    @li_blp.response(LiSchemaResponse)
    # @jwt_required()
    def get(self, args: dict):
        """License 所有License信息"""
        datas = li_service.query_by_time(args)
        return datas

    @li_blp.response(LiUploadSchemaResponse)
    def post(self):
        """数据源管理 创建数据源"""
        from flask import request
        content = request.files['file'].read().decode('ascii')
        res = li_service.is_legal(content)
        return {'msg': res}


@li_blp.route('/<int:license_id>')
class LicenseAPI(MethodView):
    """LicenseAPI"""
    decorators = [jwt_required()]

    @li_blp.response(LiDlSchemaResponse)
    def delete(self, license_id: int):
        """ 软删除 该条数据 """
        res = li_service.del_li_id(license_id)
        if res:
            return {'msg': True}
        return {'msg': False}
