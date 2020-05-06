import preset
from datetime import datetime, timezone, timedelta


def add(value):
    value[0] = value[0] + 1
    return value[0]


def check_is_none(value):
    if value is None:
        return preset.empty_string
    return str(value)


def to_number(value):
    if value != preset.empty_string and value != preset.empty and value != preset.blank and value != preset.no_date:
        return int(value)
    return None


def to_date(value):
    date_value = to_number(value)
    if date_value:
        microseconds = int(hex(int(date_value)*10)[2:17], 16) / 10
        seconds, microseconds = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 86400)
        return datetime(1601, 1, 1) + timedelta(days, seconds, microseconds)
    return preset.no_date


def date_to_string(date_value):
    if isinstance(date_value, str):
        return date_value
    if isinstance(date_value, datetime):
        return date_value.strftime(preset.date_format)
    return preset.no_date


def epoch_to_date(epoch_value):
    return (datetime(1601, 1, 1) + timedelta(microseconds=int(epoch_value))).replace(tzinfo=timezone.utc).astimezone()


def date_to_epoch(date_value):
    if date_value:
        difference = date_value - datetime(1601, 1, 1)
        seconds_in_day = 60 * 60 * 24
        value = '{:<010d}'.format(difference.days * seconds_in_day + difference.seconds + difference.microseconds)
        return str(value)
    return preset.empty


def update_tuple(tuple_object, value, position):
    list_object = list(tuple_object)
    list_object[position] = value
    return tuple(list_object)
