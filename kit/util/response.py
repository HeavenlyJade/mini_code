import json
from collections import Iterator

from flask import Flask, Response, current_app

from kit.util import json as json_util

__all__ = ['APIFlask']


class APIFlask(Flask):
    """Custom flask class."""

    json_encoder = json_util.ExtendedEncoder

    def make_response(self, rv) -> Response:
        if rv is None:
            rv = dict()

        if isinstance(rv, (list, set, Iterator)):
            return Response(
                json.dumps(list(rv), cls=json_util.ExtendedEncoder),
                mimetype=current_app.config['JSONIFY_MIMETYPE'],
            )

        return super().make_response(rv)
