# -*- coding: utf-8 -*-
# author zyy

from flask_smorest import Blueprint

license_v1_blp = Blueprint(
    'License管理', 'License', url_prefix='/api/v1/license', description='license服务接口'
)
