# -*- coding: utf-8 -*-
# author zyy

from backend.license_management.api.v1 import license_v1_blp
from backend.license_management.api.v1.license_management import li_blp

license_v1_blp.register_blueprint(li_blp)

