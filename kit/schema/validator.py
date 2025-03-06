import re

from marshmallow import ValidationError


def validate_format_datetime_str(datetime_str: str):
    """

    Notes: fmt is `yyyy-mm-dd hh:mm:ss`

    """
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

    if not re.match(pattern, datetime_str):
        raise ValidationError('时间格式不正确')
