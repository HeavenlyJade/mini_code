from flask_smorest import Blueprint


class APIBlueprint(Blueprint):
    def response(
        self,
        schema=None,
        status_code=200,
        *,
        content_type=None,
        description=None,
        example=None,
        examples=None,
        headers=None,
    ):
        return super().response(
            status_code,
            schema,
            content_type=content_type,
            description=description,
            example=example,
            examples=examples,
            headers=headers,
        )
