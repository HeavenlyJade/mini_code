from flask.views import MethodView

from backend.mini_core.schema.card import (
    Card,CardQueryArgSchema,ReCardSchema
)
from backend.mini_core.service import card_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('mini_core', 'mini_core', url_prefix='/')


@blp.route('/card')
class LogAPI(MethodView):
    """ 个人名片API"""

    @blp.arguments(CardQueryArgSchema, location='query')
    @blp.response(ReCardSchema)
    def get(self, args: dict):
        """查看个人名片"""
        return card_service.get(args)

    @blp.arguments(Card)
    @blp.response(ReCardSchema)
    def post(self, card):
        """ 新增个人名片"""
        return card_service.update(card["openid"],card)
