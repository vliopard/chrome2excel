import preset
from datetime import datetime, timezone, timedelta


def add(value):
    value[0] = value[0] + 1
    return value[0]


def get(value):
    return value[0]


def check_is_none(value):
    return preset.EMPTY_STRING if value is None else str(value)


def to_number(value):
    if value != preset.EMPTY_STRING and value != preset.EMPTY and value != preset.BLANK and value != preset.NO_DATE:
        return int(value)
    return None


def to_date(value):
    date_value = to_number(value)
    if date_value:
        microseconds = int(hex(int(date_value)*10)[2:17], 16) / 10
        seconds, microseconds = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 86400)
        return datetime(1601, 1, 1) + timedelta(days, seconds, microseconds)
    return preset.NO_DATE


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
    return preset.EMPTY


def update_tuple(tuple_object, value, position):
    list_object = list(tuple_object)
    list_object[position] = value
    return tuple(list_object)


def update_progress(message, index, total_items):
    if preset.gui_progress_dialog:
        if index < 0:
            preset.gui_progress_dialog.SetLabel(message)
            preset.gui_progress_dialog.SetRange(total_items)
        else:
            progress_dialog_not_cancelled, _ = preset.gui_progress_dialog.Update(index, str(int(index / total_items * 100)) + "%  [ " + str(index) + " / " + str(total_items) + " ]")
            if not progress_dialog_not_cancelled:
                return True
    return False


def process_tree(children_list, count):
    for item in children_list:
        if "type" in item and item["type"] == "url":
            count += 1
        if "type" in item and item["type"] == "folder":
            if "children" in item:
                count = process_tree(item["children"], count)
    return count


def count_urls(items):
    count = 0
    for key, value in items:
        if "children" in value:
            count = process_tree(value["children"], count)
    return count


def key_on_substring(dictionary_data, text_substring):
    for dictionary_key in dictionary_data:
        if dictionary_key in text_substring:
            return dictionary_key
    return None


def contains(single_element, list_of_elements):
    return any(element in single_element for element in list_of_elements)


def check_fragment(in_string, url):
    return_list = []
    string_list = in_string.split('&')
    for string_item in string_list:
        token = string_item.split('=')[0]
        if token.startswith('D['):
            token = 'D['
        if not contains(token, preset.dict_params[key_on_substring(preset.dict_params, url)] + preset.general_params if key_on_substring(preset.dict_params, url) else preset.general_params):
            return_list.append(string_item)
    return "&".join(return_list)
