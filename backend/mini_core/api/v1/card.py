from flask.views import MethodView
from flask import request

from backend.mini_core.schema.card import (
    Card, CardQueryArgSchema, ReCardSchema, CardUserSchema, ReCardSchemaList,CardSchema
)
from backend.mini_core.service import card_service
from kit.util.blueprint import APIBlueprint

blp = APIBlueprint('mini_core', 'mini_core', url_prefix='/')


@blp.route('/card_list')
class CardList(MethodView):
    """ 名片列表API """

    @blp.arguments(CardUserSchema, location='query')
    @blp.response(ReCardSchemaList)
    def get(self, args: dict):
        """查看名片列表"""
        return card_service.card_list(args)


@blp.route('/card')
class CardAPI(MethodView):
    """ 个人名片API """

    @blp.arguments(CardQueryArgSchema, location='query')
    @blp.response(ReCardSchema)
    def get(self, args: dict):
        """根据openid查看个人名片"""
        return card_service.get(args)

    @blp.arguments(CardSchema)
    @blp.response(ReCardSchema)
    def post(self, card):
        """新增个人名片"""
        return card_service.create(card)

    @blp.arguments(CardSchema)
    @blp.response(ReCardSchema)
    def put(self, card):
        """修改个人名片"""
        card_id = request.json.get('id')
        return card_service.update(card_id, card)

    @blp.arguments(CardQueryArgSchema)
    @blp.response(ReCardSchema)
    def delete(self, args):
        """删除个人名片"""
        card_id = request.json.get('id')
        return card_service.delete(card_id)
