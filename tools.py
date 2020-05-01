import os
import preset

from platform import system

#######################################################################################
# TODO: LOAD DEBUG SETTINGS FROM DEBUG FILE
#######################################################################################


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
    argument_count = len(arguments)
    if argument_count > 0:
        text = preset.empty
        for element in arguments:
            text = text + element + preset.blank
        text = text.rstrip()
        print(text)
    else:
        return 0


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
