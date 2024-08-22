import json
import tools
import utils
import public
import preset
import html_support
from utils import timed

from configparser import ConfigParser, DuplicateSectionError


@public.add
class Options:
    def __init__(self):
        self.system_language = preset.ENGLISH
        self.debug_system = False
        self.export_file_type = False
        self.refresh_url_title = False
        self.remove_duplicated_urls = False
        self.remove_tracking_tokens_from_url = False
        self.display_exit_dialog = False
        self.refresh_folder_name_with_hostname_title = False
        self.exit_dialog_confirmation = True
        self.configuration_category = preset.MAIN_SECTION
        self.configuration_parser = ConfigParser()
        self.configuration_parser.read(preset.CONFIGURATION_FILENAME)

    def save_settings(self):
        try:
            self.configuration_parser.add_section(self.configuration_category)
        except DuplicateSectionError:
            pass

        self.exit_dialog_confirmation = self.display_exit_dialog

        self.configuration_parser.set(self.configuration_category, preset.DEBUG_SYSTEM, str(preset.DEBUG_MODE))
        self.configuration_parser.set(self.configuration_category, preset.LOAD_TIME_OUT, str(preset.TIMEOUT))
        self.configuration_parser.set(self.configuration_category, preset.system_language, str(self.system_language))
        self.configuration_parser.set(self.configuration_category, preset.export_file_type, str(self.export_file_type))
        self.configuration_parser.set(self.configuration_category, preset.refresh_url_title, str(self.refresh_url_title))
        self.configuration_parser.set(self.configuration_category, preset.remove_duplicated_urls, str(self.remove_duplicated_urls))
        self.configuration_parser.set(self.configuration_category, preset.remove_tracking_tokens_from_url, str(self.remove_tracking_tokens_from_url))
        self.configuration_parser.set(self.configuration_category, preset.display_exit_dialog, str(self.display_exit_dialog))
        self.configuration_parser.set(self.configuration_category, preset.refresh_folder_name_with_hostname_title, str(self.refresh_folder_name_with_hostname_title))
        self.configuration_parser.set(self.configuration_category, preset.exit_dialog_confirmation, str(self.exit_dialog_confirmation))
        with open(preset.CONFIGURATION_FILENAME, 'w') as configuration_file:
            self.configuration_parser.write(configuration_file)
        if preset.DEBUG_MODE:
            preset.RUN_GUI = False

    def load_settings(self):
        try:
            preset.DEBUG_MODE = self.configuration_parser.getboolean(self.configuration_category, preset.DEBUG_SYSTEM)
            preset.TIMEOUT = self.configuration_parser.getint(self.configuration_category, preset.LOAD_TIME_OUT)
            self.system_language = self.configuration_parser.get(self.configuration_category, preset.system_language)
            self.export_file_type = self.configuration_parser.getboolean(self.configuration_category, preset.export_file_type)
            self.refresh_url_title = self.configuration_parser.getboolean(self.configuration_category, preset.refresh_url_title)
            self.remove_duplicated_urls = self.configuration_parser.getboolean(self.configuration_category, preset.remove_duplicated_urls)
            self.remove_tracking_tokens_from_url = self.configuration_parser.getboolean(self.configuration_category, preset.remove_tracking_tokens_from_url)
            self.display_exit_dialog = self.configuration_parser.getboolean(self.configuration_category, preset.display_exit_dialog)
            self.refresh_folder_name_with_hostname_title = self.configuration_parser.getboolean(self.configuration_category, preset.refresh_folder_name_with_hostname_title)
            self.exit_dialog_confirmation = self.configuration_parser.getboolean(self.configuration_category, preset.exit_dialog_confirmation)

        except Exception as exc:
            print(f'Using default values [{exc}]')
            preset.TIMEOUT = 10
            preset.DEBUG_MODE = False
            self.system_language = preset.ENGLISH
            self.export_file_type = False
            self.refresh_url_title = False
            self.remove_duplicated_urls = False
            self.remove_tracking_tokens_from_url = False
            self.display_exit_dialog = False
            self.refresh_folder_name_with_hostname_title = False
            self.exit_dialog_confirmation = True

        if preset.DEBUG_MODE:
            preset.RUN_GUI = False
        preset.set_language(self.system_language)


@public.add
class Item(dict):

    @property
    def id(self):
        return self[preset.ITEM_ID]

    @property
    def name(self):
        return self[preset.ITEM_NAME]

    @property
    def type(self):
        return self[preset.BOOKMARKS_TYPE]

    @property
    def url(self):
        if preset.BOOKMARKS_URL in self:
            return self[preset.BOOKMARKS_URL]
        return ''

    @property
    def icon(self):
        if preset.ITEM_ICON in self:
            return self[preset.ITEM_ICON]
        return preset.SYMBOL_EMPTY

    @property
    def added(self):
        return utils.epoch_to_date(self[preset.ITEM_DATE_ADDED])

    @property
    def modified(self):
        if preset.ITEM_DATE_MODIFIED in self:
            return utils.epoch_to_date(self[preset.ITEM_DATE_MODIFIED])

    @property
    def folders(self):
        items = []
        for children in self[preset.BOOKMARKS_CHILDREN]:
            if children[preset.BOOKMARKS_TYPE] == preset.BOOKMARKS_FOLDER:
                items.append(Item(children))
        return items

    @property
    def urls(self):
        items = []
        for children in self[preset.BOOKMARKS_CHILDREN]:
            if children[preset.BOOKMARKS_TYPE] == preset.BOOKMARKS_URL:
                items.append(Item(children))
        return items


@public.add
class Bookmarks:
    path = None

    def __init__(self, path):
        self.path = path
        self.data = json.loads(open(path, encoding=preset.CHARSET_UTF8).read())
        self.attrList = self.process_roots()
        self.urls = self.attrList[preset.BOOKMARKS_URLS]
        self.folders = self.attrList[preset.BOOKMARKS_FOLDERS]
        self.length = utils.count_urls(self.data[preset.BOOKMARKS_ROOTS].items())

    def process_roots(self):
        attribute_list = {preset.BOOKMARKS_URLS: [], preset.BOOKMARKS_FOLDERS: []}
        for key, value in self.data[preset.BOOKMARKS_ROOTS].items():
            if preset.BOOKMARKS_CHILDREN in value:
                self.process_tree(attribute_list, value[preset.BOOKMARKS_CHILDREN])
        return attribute_list

    def process_tree(self, attribute_list, children_list):
        for item in children_list:
            if preset.BOOKMARKS_TYPE in item and item[preset.BOOKMARKS_TYPE] == preset.BOOKMARKS_URL:
                attribute_list[preset.BOOKMARKS_URLS].append(Item(item))
            if preset.BOOKMARKS_TYPE in item and item[preset.BOOKMARKS_TYPE] == preset.BOOKMARKS_FOLDER:
                attribute_list[preset.BOOKMARKS_FOLDERS].append(Item(item))
                if preset.BOOKMARKS_CHILDREN in item:
                    self.process_tree(attribute_list, item[preset.BOOKMARKS_CHILDREN])


def read_content(folder_items):
    url_list = []
    for folder_item in folder_items:
        url_date_added = preset.SYMBOL_EMPTY
        url_date_modified = preset.SYMBOL_EMPTY
        url_guid = preset.SYMBOL_EMPTY
        url_item_id = preset.SYMBOL_EMPTY
        url_last_visited = preset.SYMBOL_EMPTY
        url_name = preset.SYMBOL_EMPTY
        url_sync_transaction_version = preset.SYMBOL_EMPTY
        url_item_type = preset.SYMBOL_EMPTY
        url_address = preset.SYMBOL_EMPTY
        url_icon = preset.SYMBOL_EMPTY
        for item in folder_item:
            if item == preset.BOOKMARKS_CHILDREN:
                read_content(folder_item[item])
            elif item == preset.META_INFO:
                for element in folder_item[item]:
                    if element == preset.LAST_VISITED:
                        url_last_visited = folder_item[item][element]
            elif item == preset.ITEM_DATE_ADDED:
                url_date_added = folder_item[item]
            elif item == preset.ITEM_DATE_MODIFIED:
                url_date_modified = folder_item[item]
            elif item == preset.GUID:
                url_guid = folder_item[item]
            elif item == preset.ITEM_ICON:
                url_icon = folder_item[item]
            elif item == preset.ITEM_ID:
                url_item_id = folder_item[item]
            elif item == preset.ITEM_NAME:
                url_name = folder_item[item]
            elif item == preset.SYNC_TRANSACTION_VERSION:
                url_sync_transaction_version = folder_item[item]
            elif item == preset.ITEM_TYPE:
                url_item_type = folder_item[item]
            elif item == preset.BOOKMARKS_URL:
                url_address = folder_item[item].strip()
            else:
                tools.print_debug(preset.MESSAGE[preset.WARNING] + str(item))
        parsed_url = dict()
        parsed_url[preset.URL_INFO_GUID] = url_guid
        parsed_url[preset.URL_INFO_ITEM_ID] = url_item_id
        parsed_url[preset.URL_INFO_SYNC_TRANSACTION_VERSION] = url_sync_transaction_version
        parsed_url[preset.URL_INFO_ITEM_TYPE] = url_item_type
        parsed_url[preset.URL_INFO_DATE_ADDED] = utils.to_date(url_date_added)
        parsed_url[preset.URL_INFO_DATE_MODIFIED] = utils.to_date(url_date_modified)
        parsed_url[preset.URL_INFO_LAST_VISITED] = utils.to_date(url_last_visited)

        if preset.CLEAN_URL_BOOL:
            clean_url = html_support.parse_url_clean(url_address)
        else:
            clean_url = url_address
        parsed_url[preset.URL_INFO_PARSE_ADDRESS] = clean_url
        parsed_url[preset.URL_INFO_PRIME_ADDRESS] = preset.SYMBOL_EMPTY if url_address == clean_url and preset.CLEAN_URL_BOOL else url_address
        parsed_url[preset.URL_INFO_UNDUP_ADDRESS] = f'{parsed_url[preset.URL_INFO_PARSE_ADDRESS]} {parsed_url[preset.URL_INFO_PRIME_ADDRESS]}'.strip()

        if preset.REFRESH_TITLE:
            parsed_url[preset.URL_INFO_NAME_PREVIOUS] = url_name
            parsed_url[preset.URL_INFO_NAME] = html_support.get_stored_link(clean_url)
        else:
            parsed_url[preset.URL_INFO_NAME_PREVIOUS] = preset.NO_PREVIOUS_TITLE
            parsed_url[preset.URL_INFO_NAME] = url_name

        parsed_url[preset.URL_INFO_ICON] = url_icon

        parsed_url = parsed_url | html_support.parse_url(url_address)
        url_list.append(parsed_url)
    return url_list


def generate_bookmarks(profile):
    tools.print_display(preset.MESSAGE[preset.GENERATING_BOOKMARKS])
    bookmarks_file = tools.get_chrome_element(profile, preset.BOOKMARKS)
    if bookmarks_file:
        return Bookmarks(bookmarks_file)
    return None


@timed
def generate_data(instance):
    data_header = []
    for folder in instance.folders:
        folder_item = None
        folder_date_added = preset.NO_DATE
        folder_date_modified = preset.NO_DATE
        folder_guid = preset.SYMBOL_EMPTY
        folder_id = preset.SYMBOL_EMPTY
        folder_last_visited = preset.NO_DATE
        folder_name = preset.SYMBOL_EMPTY
        folder_sync_transaction_version = preset.SYMBOL_EMPTY
        folder_type = preset.SYMBOL_EMPTY
        folder_url = preset.SYMBOL_EMPTY
        for item in folder:
            if item == preset.BOOKMARKS_CHILDREN:
                folder_item = read_content(folder[item])
            elif item == preset.META_INFO:
                for element in folder[item]:
                    if element == preset.LAST_VISITED:
                        folder_last_visited = folder[item][element]
            elif item == preset.ITEM_DATE_ADDED:
                folder_date_added = folder[item]
            elif item == preset.ITEM_DATE_MODIFIED:
                folder_date_modified = folder[item]
            elif item == preset.GUID:
                folder_guid = folder[item]
            elif item == preset.ITEM_ID:
                folder_id = folder[item]
            elif item == preset.ITEM_NAME:
                folder_name = folder[item]
            elif item == preset.SYNC_TRANSACTION_VERSION:
                folder_sync_transaction_version = folder[item]
            elif item == preset.ITEM_TYPE:
                folder_type = folder[item]
            elif item == preset.BOOKMARKS_URL:
                folder_url = folder[item]
            else:
                tools.print_debug(preset.MESSAGE[preset.WARNING] + str(item))
        folder_data = {
                preset.FOLDER_INFO_GUID: folder_guid,
                preset.FOLDER_INFO_ID: folder_id,
                preset.FOLDER_INFO_SYNC_TRANSACTION_VERSION: folder_sync_transaction_version,
                preset.FOLDER_INFO_TYPE: folder_type,
                preset.FOLDER_INFO_DATE_ADDED: utils.to_date(folder_date_added),
                preset.FOLDER_INFO_DATE_MODIFIED: utils.to_date(folder_date_modified),
                preset.FOLDER_INFO_LAST_VISITED: utils.to_date(folder_last_visited),
                preset.FOLDER_INFO_NAME: folder_name,
                preset.FOLDER_INFO_URL: folder_url
        }
        for item in folder_item:
            folder_data_complete = folder_data | item
            data_header.append(folder_data_complete)
    return data_header
