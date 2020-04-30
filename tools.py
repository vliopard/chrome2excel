from datetime import datetime, timezone, timedelta

#######################################################################################
# TODO: LOAD DEBUG SETTINGS FROM DEBUG FILE
#######################################################################################

debug_mode = False


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


def display(*arguments):
    argument_count = len(arguments)
    if argument_count > 0:
        text = ""
        for element in arguments:
            text = text + element + " "
        text = text.rstrip()
        print(text)
    else:
        return 0


def debug(*arguments):
    if debug_mode:
        argument_count = len(arguments)
        if argument_count > 0:
            text = ""
            for element in arguments:
                text = text + element + " "
            text = text.rstrip()
            print(text)
        else:
            return 0


def add(value):
    value[0] = value[0] + 1
    return value[0]


def check_is_none(value):
    if value is None:
        return '[Empty]'
    return str(value)


def to_number(value):
    if value != '[Empty]':
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
        return "None"
    return date_value.strftime("%Y/%m/%d, %H:%M:%S")


def epoch_to_date(epoch_value):
    return (datetime(1601, 1, 1) + timedelta(microseconds=int(epoch_value))).replace(tzinfo=timezone.utc).astimezone()


def date_to_epoch(date_value):
    if date_value:
        difference = date_value - datetime(1601, 1, 1)
        seconds_in_day = 60 * 60 * 24
        value = '{:<010d}'.format(difference.days * seconds_in_day + difference.seconds + difference.microseconds)
        return str(value)
    return ""
