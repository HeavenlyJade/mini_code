"""Custom Sqlalchemy Hook."""
import sys
import time

import oracledb

oracledb.version = '8.3.0'
sys.modules['cx_Oracle'] = oracledb

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, inspect
from sqlalchemy.orm import Query


from .base import BaseHook

__all__ = ['SqlAHook']

from kit.domain.entity import SoftDeleteMixin


class SqlAHook(SQLAlchemy, BaseHook):
    """SQLAlchemy hook to interact with database"""

    def init_app(self, app: Flask):
        super(SqlAHook, self).init_app(app)

    def apply_pool_defaults(self, app, options) -> dict:
        options = super().apply_pool_defaults(app, options)
        options['pool_pre_ping'] = True
        return options


@event.listens_for(Query, 'before_compile', retval=True)
def soft_delete_query(query):
    for desc in query.column_descriptions:
        entity = desc['entity']
        if entity is None:
            continue

        inspector = inspect(desc['entity'])
        mapper = getattr(inspector, 'mapper', None)
        if mapper and issubclass(mapper.class_, SoftDeleteMixin):
            query = query.enable_assertions(False).filter(entity.delete_time == 0)
            break
    return query


@event.listens_for(Query, 'before_compile_delete', retval=True)
def soft_delete(query, delete_context):
    from backend.extensions import db

    for desc in query.column_descriptions:
        if issubclass(desc['type'], SoftDeleteMixin):
            entity = desc['entity']
            query = query.filter(entity.delete_time == 0)
            query.update(dict(delete_time=int(time.time())))
            # TODO replace it
            return None
