import datetime as dt

from dateutil.parser import parse


def datetime_format(obj, fmt='%Y-%m-%d %H:%M:%S'):
    if obj is None:
        return obj

    if isinstance(obj, str):
        return dt.datetime.strptime(obj, fmt)
    else:
        return obj.strftime(fmt)


def datetime_str_to_ts(datetime_str: str) -> int:
    return int(parse(datetime_str).timestamp())


def datetime_range(start_time: dt.datetime, end_time: dt.datetime, delta: dt.timedelta):
    while start_time <= end_time:
        yield start_time
        start_time += delta


def faster_datetime2str(datetime: dt.datetime) -> str:
    month = _zero_filled_number(datetime.month)
    day = _zero_filled_number(datetime.day)
    hour = _zero_filled_number(datetime.hour)
    minute = _zero_filled_number(datetime.minute)
    second = _zero_filled_number(datetime.second)
    return f'{datetime.year}-{month}-{day} {hour}:{minute}:{second}'


def _zero_filled_number(number: int):
    return number if number >= 10 else f'0{number}'


def to_milli_time(timestamp: float) -> int:
    return round(timestamp * 1000)


def from_milli_time_to_datetime(milli_time: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(milli_time / 1000)


def get_datetime_with_milli_from_time(milli_time: int) -> str:
    return datetime_format(
        dt.datetime.fromtimestamp(milli_time / 1000),
        fmt='%Y-%m-%d %H:%M:%S.%f'
    )[:-3]



