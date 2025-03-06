# -*- coding: utf-8 -*-
# author zyy
from backend.extensions import db
# from .mock import LiMockRepository
from .sqla import LiSQLARepository

# TODO replace this with DI
li_mock_repo = LiSQLARepository(db.session)
