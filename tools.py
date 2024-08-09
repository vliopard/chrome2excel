import os
import json
import preset
import screenSupport

from platform import system


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
        print('\n')
        double_line()
        double_line("DEBUG MESSAGE START")
        double_line()
        print_display(*arguments)
        double_line()
        double_line("DEBUG MESSAGE END")
        double_line()
        print('\n')


def print_display(*arguments):
    if not preset.RUN_GUI:
        argument_count = len(arguments)
        if argument_count > 0:
            display_text = preset.EMPTY
            for element in arguments:
                display_text = display_text + str(element) + preset.BLANK
            display_text = display_text.rstrip()
            if display_text != "default":
                print(display_text)
        else:
            return 0


def highlight(*arguments):
    print('\n\n')
    print_overline()
    print_display(*arguments)
    print_underline()
    print('\n\n')


def print_underline():
    print_display(preset.UNDERLINE * (screenSupport.get_terminal_width()))


def print_overline():
    print_display(preset.OVERLINE * (screenSupport.get_terminal_width()))


def double_line(message=None):
    if message:
        message = "== " + message + " "
        print_display(message + "=" * (screenSupport.get_terminal_width() - len(message)))
    else:
        print_display("=" * (screenSupport.get_terminal_width()))


def select_profile(profile):
    profile = str(profile)
    if profile == "0":
        profile = "Default"
    else:
        profile = "Profile " + profile
    return profile


def get_chrome_element(profile_number, item):
    computer = system()
    profile_name = select_profile(profile_number)
    chrome_file = preset.EMPTY
    if computer == "Windows":
        chrome_file = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\" + profile_name + "\\" + item)
    if computer == "Linux":
        chrome_file = os.path.expanduser("~/.config/google-chrome/" + profile_name + "/" + item)
    if computer == "Darwin":
        chrome_file = os.path.expanduser("~/Library/Application Support/Google/Chrome/" + profile_name + "/" + item)
    if os.path.exists(chrome_file):
        return chrome_file
    return None


def get_user(user_path):
    user_name = json.loads(open(user_path, encoding=preset.UTF8).read())["account_info"][0]
    return user_name['email'], user_name['full_name'], user_name['given_name']


def retrieve_profile(profile):
    user_data = get_chrome_element(profile, preset.PREFERENCES)
    if not user_data:
        raise Exception(preset.message["invalid_profile"])
    return get_user(user_data)


def get_profile_list():
    user_list = []
    for number in range(0, 100):
        try:
            email, full_name, display_name = retrieve_profile(number)
            user_list.append([number, full_name + " - " + email])
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
        print_display(f'{preset.message["user"]}{show_var}: {left_justified_name.ljust(35)} [{email}]')
    except Exception as error:
        if not dig:
            print_display(error)
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
