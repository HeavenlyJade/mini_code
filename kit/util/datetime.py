import datetime as dt
from typing import Type,Union
from dateutil.parser import parse
from kit.domain.entity import Entity, EntityInt

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


def timestamp_to_datetime(timestamp: int) -> dt.datetime:
    """
    将时间戳转换为datetime对象，如果时间戳为None则返回None

    Args:
        timestamp: Unix时间戳（秒），可以是整数、浮点数或None

    Returns:
        datetime对象或None
    """
    if timestamp is None:
        return None
    return dt.datetime.fromtimestamp(timestamp)


def convert_timestamps_to_datetime(data: Union[Type[Entity], Type[EntityInt]]):
    """
    将数据对象中的时间戳字段转换为datetime对象

    参数:
        data: 包含create_time、update_time和delete_time时间戳字段的对象

    返回:
        更新后的相同对象，时间戳已转换为datetime
    """
    data.create_time = timestamp_to_datetime(data.create_time)
    data.update_time = timestamp_to_datetime(data.update_time)
    data.delete_time = timestamp_to_datetime(data.delete_time)
    return data

def get_datetime_with_milli_from_time(milli_time: int) -> str:
    return datetime_format(
        dt.datetime.fromtimestamp(milli_time / 1000),
        fmt='%Y-%m-%d %H:%M:%S.%f'
    )[:-3]



