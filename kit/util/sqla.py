from flask import current_app
from sqlalchemy import BigInteger, Column, Identity, Text, TypeDecorator
from flask_jwt_extended import get_current_user
from kit.util import json as json_util
from kit.exceptions import ServiceBadRequest

class JsonText(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""

    impl = Text

    def process_bind_param(self, value, dialect):
        return json_util.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return json_util.loads(value)


def id_column():
    if current_app.config['DATABASE_TYPE'] == 'oracle':
        return Column(
            'id', BigInteger, Identity(start=1, increment=1), primary_key=True
        )

    return Column('id', BigInteger, primary_key=True)


def validate_user_entity_match(entity_id):
    user_cache = get_current_user()
    user_id_cache = user_cache.id
    if user_id_cache != entity_id:
        raise ServiceBadRequest("错误的请求用户")
