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


def debug(*arguments):
    if preset.debug_mode:
        display(*arguments)


def display(*arguments):
    if not preset.run_gui:
        argument_count = len(arguments)
        if argument_count > 0:
            display_text = preset.empty
            for element in arguments:
                display_text = display_text + str(element) + preset.blank
            display_text = display_text.rstrip()
            if display_text != "default":
                print(display_text)
        else:
            return 0


def underline():
    display(preset.underline*(screenSupport.get_terminal_width()))


def overline():
    display(preset.overline*(screenSupport.get_terminal_width()))


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
    chrome_file = preset.empty
    if computer == "Windows":
        chrome_file = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\" + profile_name + "\\" + item)
    if computer == "Linux":
        chrome_file = os.path.expanduser("~/.config/google-chrome/" + profile_name + "/" + item)
    if computer == "Darwin":
        chrome_file = os.path.expanduser("~/Library/Application Support/Google/Chrome/" + profile_name + "/" + item)
    if os.path.exists(chrome_file):
        return chrome_file
    return None


def get_settings(settings):
    refresh = preset.off
    if settings.refresh_url_title:
        refresh = preset.on

    undupe = preset.off
    if settings.remove_duplicated_urls:
        undupe = preset.on

    clean = preset.off
    if settings.remove_tracking_tokens_from_url:
        clean = preset.on

    get_hostname_title = preset.off
    if settings.refresh_folder_name_with_hostname_title:
        get_hostname_title = preset.on

    return refresh, undupe, clean, get_hostname_title


def get_user(user_path):
    user_name = json.loads(open(user_path, encoding='utf-8').read())["account_info"][0]
    return user_name['email'], user_name['full_name'], user_name['given_name']


def retrieve_profile(profile):
    user_data = get_chrome_element(profile, preset.preferences)
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


def list_profiles(profile):
    if profile == preset.all_profiles:
        for number in range(0, 100):
            try:
                email, full_name, display_name = retrieve_profile(number)
                if len(full_name) < 20:
                    tab = preset.tab
                else:
                    tab = preset.empty
                display(preset.message["user"] + "[" + str(number) + "]: {", full_name, "}" + preset.tab + tab + " [", email, "]")
            except Exception:
                pass
    else:
        try:
            email, full_name, display_name = retrieve_profile(profile)
            display(preset.message["user"] + ": {", full_name, "} [" + email + "]")
        except Exception as error:
            display(error)


def get_system():
    return system()
