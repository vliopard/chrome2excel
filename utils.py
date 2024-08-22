import time
import preset
from functools import wraps
from datetime import datetime, timezone, timedelta


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time_report = [f'Start time: {start_time}', f'End time:   {end_time}', f"Function {func.__name__} ran in {timedelta(seconds=(time_end - time_start))}"]
        print(preset.SYMBOL_EQ * 100)
        for time_detail in time_report:
            print(time_detail)
        print(preset.SYMBOL_EQ * 100)
        return result
    return wrapper


def to_number(value):
    if value != preset.EMPTY_STRING and value != preset.SYMBOL_EMPTY and value != preset.SYMBOL_BLANK and value != preset.NO_DATE:
        return int(value)
    return None


def to_date(value):
    date_value = to_number(value)
    if date_value:
        microseconds = int(hex(int(date_value)*10)[2:17], 16) / 10
        seconds, microseconds = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 86400)
        return datetime(1601, 1, 1) + timedelta(days, seconds, microseconds)
    return preset.SYMBOL_EMPTY


def date_to_string(date_value):
    if isinstance(date_value, str):
        return date_value
    if isinstance(date_value, datetime):
        return date_value.strftime(preset.DATE_FORMAT)
    return preset.NO_DATE


def epoch_to_date(epoch_value):
    return (datetime(1601, 1, 1) + timedelta(microseconds=int(epoch_value))).replace(tzinfo=timezone.utc).astimezone()


def date_to_epoch(date_value):
    if isinstance(date_value, datetime):
        difference = date_value - datetime(1601, 1, 1)
        seconds_in_day = 60 * 60 * 24
        value = '{:<010d}'.format(difference.days * seconds_in_day + difference.seconds + difference.microseconds)
        return str(value)
    return preset.SYMBOL_EMPTY


def update_progress(message, index, total_items):
    if preset.GUI_PROGRESS_DIALOG:
        if index < 0:
            preset.GUI_PROGRESS_DIALOG.SetLabel(message)
            preset.GUI_PROGRESS_DIALOG.SetRange(total_items)
        else:
            progress_dialog_not_cancelled, _ = preset.GUI_PROGRESS_DIALOG.Update(index, str(int(index / total_items * 100)) + "%  [ " + str(index) + " / " + str(total_items) + " ]")
            if not progress_dialog_not_cancelled:
                return True
    return False


def process_tree(children_list, count):
    for item in children_list:
        if preset.BOOKMARKS_TYPE in item and item[preset.BOOKMARKS_TYPE] == preset.BOOKMARKS_URL:
            count += 1
        if preset.BOOKMARKS_TYPE in item and item[preset.BOOKMARKS_TYPE] == preset.BOOKMARKS_FOLDER:
            if preset.BOOKMARKS_CHILDREN in item:
                count = process_tree(item[preset.BOOKMARKS_CHILDREN], count)
    return count


def count_urls(items):
    count = 0
    for key, value in items:
        if preset.BOOKMARKS_CHILDREN in value:
            count = process_tree(value[preset.BOOKMARKS_CHILDREN], count)
    return count


def key_on_substring(dictionary_data, text_substring):
    for dictionary_key in dictionary_data:
        if dictionary_key in text_substring:
            return dictionary_key
    return None


def contains(single_element, list_of_elements):
    return any(element == single_element for element in list_of_elements)


def check_fragment(in_string, url):
    return_list = []
    string_list = in_string.split(preset.SYMBOL_AMP)
    for string_item in string_list:
        token = string_item.split(preset.SYMBOL_EQ)[0]
        if token.startswith(preset.DTOKEN):
            token = preset.DTOKEN
        key_res = key_on_substring(preset.dict_params, url)
        if not contains(token, preset.dict_params[key_res] + preset.dict_params[preset.TRACKING_MODULE] if key_res else preset.dict_params[preset.GENERAL] + preset.dict_params[preset.TRACKING_MODULE]):
            return_list.append(string_item)
    return preset.SYMBOL_AMP.join(return_list)


def to_tuple(dictionary):
    item_list = []
    for item in dictionary:
        item_list.append(dictionary[item])
    return tuple(item_list)
