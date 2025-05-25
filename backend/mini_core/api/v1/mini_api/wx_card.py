from flask.views import MethodView
from flask import request

from backend.mini_core.schema.card import (
    Card, CardQueryArgSchema, ReCardSchema, CardUserSchema, ReCardSchemaList,CardSchema
)
from backend.mini_core.service import card_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('card', 'card', url_prefix='/card')

@blp.route('/')
class CardAPI(MethodView):
    """ 个人名片API """

    @blp.arguments(CardQueryArgSchema, location='query')
    @blp.response(ReCardSchema)
    def get(self, args: dict):
        """根据user_id查看个人名片"""
        return card_service.get(args)

