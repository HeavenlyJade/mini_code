import datetime as dt
import decimal
import json
from dataclasses import asdict
from typing import Any

from kit.domain.entity import Entity


class ExtendedEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, dt.date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, Entity):
            return asdict(o)
        return json.JSONEncoder.default(self, o)


def dumps(obj: Any, ensure_ascii: bool = False) -> str:
    return json.dumps(obj, ensure_ascii=ensure_ascii, cls=ExtendedEncoder)


def loads(obj: str) -> dict:
    return json.loads(obj)

