import os
import json
import time
import preset
import screen_support

from platform import system
from functools import wraps
from datetime import datetime, timedelta


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


def print_debug(*arguments):
    if preset.DEBUG_MODE:
        print(preset.NEW_LINE)
        double_line()
        double_line(preset.TEXT_DEBUG_MESSAGE_START)
        double_line()
        print_display(*arguments)
        double_line()
        double_line(preset.TEXT_DEBUG_MESSAGE_END)
        double_line()
        print(preset.NEW_LINE)


def print_box(msg):
    print_underline()
    print_display(msg)
    print_overline()


def print_display(*arguments):
    if not preset.RUN_GUI:
        argument_count = len(arguments)
        if argument_count > 0:
            display_text = preset.SYMBOL_EMPTY
            for element in arguments:
                display_text = display_text + str(element) + preset.SYMBOL_BLANK
            display_text = display_text.rstrip()
            if display_text != preset.DEFAULT_L:
                print(display_text)
        else:
            return 0


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time_report = [f'Start time: {start_time}', f'End time:   {end_time}', f"Function {func.__name__} ran in {timedelta(seconds=(time_end - time_start))}"]
        print(f'{section_line(preset.SYMBOL_EQ, preset.LINE_LEN)}')
        for time_detail in time_report:
            print(time_detail)
        print(f'{section_line(preset.SYMBOL_EQ, preset.LINE_LEN)}')
        return result
    return wrapper


def section_line(style, size):
    return style * size


def print_underline():
    print_display(preset.SYMBOL_UNDERLINE * (screen_support.get_terminal_width()))


def print_overline():
    print_display(preset.SYMBOL_OVERLINE * (screen_support.get_terminal_width()))


def double_line(message=None):
    if message:
        message = f'== {message} '
        print_display(message + preset.SYMBOL_EQ * (screen_support.get_terminal_width() - len(message)))
    else:
        print_display(preset.SYMBOL_EQ * (screen_support.get_terminal_width()))


def select_profile(profile):
    profile = str(profile)
    if profile == preset.SYMBOL_ZERO:
        profile = preset.DEFAULT_L
    else:
        profile = f'Profile {profile}'
    return profile


def get_chrome_element(profile_number, item):
    computer = system()
    profile_name = select_profile(profile_number)
    chrome_file = preset.SYMBOL_EMPTY
    if computer == preset.SYSTEM_WINDOWS:
        chrome_file = os.path.expanduser(f'~\\AppData\\Local\\Google\\Chrome\\User Data\\{profile_name}\\{item}')
    if computer == preset.SYSTEM_LINUX:
        chrome_file = os.path.expanduser(f'~/.config/google-chrome/{profile_name}/{item}')
    if computer == preset.SYSTEM_DARWIN:
        chrome_file = os.path.expanduser(f'~/Library/Application Support/Google/Chrome/{profile_name}/{item}')
    if os.path.exists(chrome_file):
        return chrome_file
    return None


def get_user(user_path):
    user_name = json.loads(open(user_path, encoding=preset.CHARSET_UTF8).read())[preset.ACCOUNT_INFO][0]
    return user_name[preset.EMAIL], user_name[preset.FULL_NAME], user_name[preset.GIVEN_NAME]


def retrieve_profile(profile):
    user_data = get_chrome_element(profile, preset.PREFERENCES)
    if not user_data:
        raise Exception(preset.MESSAGE[preset.INVALID_PROFILE])
    return get_user(user_data)


def get_profile_list():
    user_list = []
    for number in range(0, 100):
        try:
            email, full_name, display_name = retrieve_profile(number)
            user_list.append([number, f'{full_name} - {email}'])
        except Exception:
            pass
    return user_list


def get_display(number):
    dig = False
    if str(number).isdigit():
        dig = True

    try:
        email, full_name, display_name = retrieve_profile(number)
        left_justified_name = f'({full_name})'
        show_var = f' [{str(number)}]' if dig else ''
        print_display(f'{preset.MESSAGE[preset.USER]}{show_var}: {left_justified_name.ljust(35)} [{email}]')
    except Exception as exception:
        if not dig:
            print_display(exception)
        else:
            pass


def list_profiles(profile):
    if profile == preset.PROFILES:
        for number in range(0, 100):
            get_display(number)
    else:
        get_display(profile)


def get_system():
    return system()
