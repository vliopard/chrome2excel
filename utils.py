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
    if value != preset.empty_string:
        return int(value)
    return None


def to_date(value):
    date_value = to_number(value)
    if date_value:
        microseconds = int(hex(int(date_value)*10)[2:17], 16) / 10
        seconds, microseconds = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 86400)
        return datetime(1601, 1, 1) + timedelta(days, seconds, microseconds)
    return None


def date_to_string(date_value):
    if not date_value:
        return preset.no_date
    return date_value.strftime(preset.date_format)


def epoch_to_date(epoch_value):
    return (datetime(1601, 1, 1) + timedelta(microseconds=int(epoch_value))).replace(tzinfo=timezone.utc).astimezone()


def date_to_epoch(date_value):
    if date_value:
        difference = date_value - datetime(1601, 1, 1)
        seconds_in_day = 60 * 60 * 24
        value = '{:<010d}'.format(difference.days * seconds_in_day + difference.seconds + difference.microseconds)
        return str(value)
    return preset.empty
