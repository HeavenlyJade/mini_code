from flask import current_app
from sqlalchemy import BigInteger, Column, Identity, Text, TypeDecorator

from kit.util import json as json_util


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
