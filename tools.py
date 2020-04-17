from datetime import datetime, timezone, timedelta


class Folder:

    def __init__(
        self,
        add_date=None,
        modify_date=None,
        folder_name=None,
        children=None
    ):
        self.add_date = add_date
        self.modify_date = modify_date
        self.folder_name = folder_name
        self.children = children
    
    def add_url(self, url):
        self.children.append(url)

    def __repr__(self):
        return str(self.__dict__)


class Urls:

    def __init__(
        self,
        url=None,
        add_date=None,
        title=None
    ):
        self.url = url
        self.add_date = add_date
        self.title = title

    def __repr__(self):
        return str(self.__dict__)


def debug(msg):
    print(msg)


def checkNone(val):
    if val is None:
        return '[Empty]'
    return str(val)


def toNumber(value):
    if value != '[Empty]':
        return int(value)
    return None


def toDate(value):
    date_value = toNumber(value)
    if date_value:
        microseconds = int(hex(int(date_value)*10)[2:17], 16) / 10
        seconds, microseconds = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 86400)
        return datetime(1601, 1, 1) + timedelta(days, seconds, microseconds)
    return None


def dateFromWebkit(timestamp):
    return (datetime(1601,1,1) + timedelta(microseconds=int(timestamp))).replace(tzinfo=timezone.utc).astimezone()


def dateToWebkit(date_string):
    if date_string:
        diff = date_string - datetime(1601, 1, 1)
        seconds_in_day = 60 * 60 * 24
        value = '{:<010d}'.format(diff.days * seconds_in_day + diff.seconds + diff.microseconds)
        return str(value)
    return("")
