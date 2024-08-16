import json
import tools
import utils
import public
import preset
import html_support
import title_master

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
        self.configuration_parser.read(preset.configuration_filename)

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
        with open(preset.configuration_filename, 'w') as configuration_file:
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
            preset.TIMEOUT = 120
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
        return self["id"]

    @property
    def name(self):
        return self["name"]

    @property
    def type(self):
        return self["type"]

    @property
    def url(self):
        if "url" in self:
            return self["url"]
        return ""

    @property
    def icon(self):
        if "icon" in self:
            return self["icon"]
        return ""

    @property
    def added(self):
        return utils.epoch_to_date(self["date_added"])

    @property
    def modified(self):
        if "date_modified" in self:
            return utils.epoch_to_date(self["date_modified"])

    @property
    def folders(self):
        items = []
        for children in self["children"]:
            if children["type"] == "folder":
                items.append(Item(children))
        return items

    @property
    def urls(self):
        items = []
        for children in self["children"]:
            if children["type"] == "url":
                items.append(Item(children))
        return items


@public.add
class Bookmarks:
    path = None

    def __init__(self, path):
        self.path = path
        self.data = json.loads(open(path, encoding=preset.UTF8).read())
        self.attrList = self.process_roots()
        self.urls = self.attrList["urls"]
        self.folders = self.attrList["folders"]
        self.length = utils.count_urls(self.data["roots"].items())

    def process_roots(self):
        attribute_list = {"urls": [], "folders": []}
        for key, value in self.data["roots"].items():
            if "children" in value:
                self.process_tree(attribute_list, value["children"])
        return attribute_list

    def process_tree(self, attribute_list, children_list):
        for item in children_list:
            if "type" in item and item["type"] == "url":
                attribute_list["urls"].append(Item(item))
            if "type" in item and item["type"] == "folder":
                attribute_list["folders"].append(Item(item))
                if "children" in item:
                    self.process_tree(attribute_list, item["children"])


def read_content(folder_items):
    url_list = []
    for folder_item in folder_items:
        url_date_added = preset.EMPTY
        url_date_modified = preset.EMPTY
        url_guid = preset.EMPTY
        url_item_id = preset.EMPTY
        url_last_visited = preset.EMPTY
        url_name = preset.EMPTY
        url_sync_transaction_version = preset.EMPTY
        url_item_type = preset.EMPTY
        url_address = preset.EMPTY
        url_icon = preset.EMPTY
        for item in folder_item:
            if item == preset.CHILDREN:
                read_content(folder_item[item])
            elif item == preset.META_INFO:
                for element in folder_item[item]:
                    if element == preset.LAST_VISITED:
                        url_last_visited = folder_item[item][element]
            elif item == preset.DATE_ADDED:
                url_date_added = folder_item[item]
            elif item == preset.DATE_MODIFIED:
                url_date_modified = folder_item[item]
            elif item == preset.GUID:
                url_guid = folder_item[item]
            elif item == preset.ICON:
                url_icon = folder_item[item]
            elif item == preset.ITEM_ID:
                url_item_id = folder_item[item]
            elif item == preset.ITEM_NAME:
                url_name = folder_item[item]
            elif item == preset.SYNC_TRANSACTION_VERSION:
                url_sync_transaction_version = folder_item[item]
            elif item == preset.ITEM_TYPE:
                url_item_type = folder_item[item]
            elif item == preset.URL:
                url_address = folder_item[item]
            else:
                tools.print_debug(preset.message['warning'] + str(item))
        parsed_url = dict()
        parsed_url['url_info_guid'] = url_guid
        parsed_url['url_info_item_id'] = url_item_id
        parsed_url['url_info_sync_transaction_version'] = url_sync_transaction_version
        parsed_url['url_info_item_type'] = url_item_type
        parsed_url['url_info_date_added'] = utils.to_date(url_date_added)
        parsed_url['url_info_date_modified'] = utils.to_date(url_date_modified)
        parsed_url['url_info_last_visited'] = utils.to_date(url_last_visited)
        clean_url = html_support.parse_url_clean(url_address)
        parsed_url['url_info_parse_address'] = clean_url
        parsed_url['url_info_prime_address'] = preset.EMPTY if url_address.strip() == clean_url.strip() else url_address
        parsed_url['url_info_name'] = url_name if len(url_name.strip()) > 5 and not url_name.startswith('https://www.youtube.com/watch') else title_master.get_title_master(clean_url)
        parsed_url['url_info_icon'] = url_icon
        parsed_url1 = html_support.parse_url(url_address)
        parsed_url = parsed_url | parsed_url1
        url_list.append(parsed_url)
    return url_list


def generate_bookmarks(profile):
    tools.print_display(preset.message['generating_bookmarks'])
    bookmarks_file = tools.get_chrome_element(profile, preset.BOOKMARKS)
    if bookmarks_file:
        return Bookmarks(bookmarks_file)
    return None


def generate_data(instance):
    data_header = []
    for folder in instance.folders:
        folder_item = None
        folder_date_added = preset.NO_DATE
        folder_date_modified = preset.NO_DATE
        folder_guid = preset.EMPTY
        folder_id = preset.EMPTY
        folder_last_visited = preset.NO_DATE
        folder_name = preset.EMPTY
        folder_sync_transaction_version = preset.EMPTY
        folder_type = preset.EMPTY
        folder_url = preset.EMPTY
        for item in folder:
            if item == preset.CHILDREN:
                folder_item = read_content(folder[item])
            elif item == preset.META_INFO:
                for element in folder[item]:
                    if element == preset.LAST_VISITED:
                        folder_last_visited = folder[item][element]
            elif item == preset.DATE_ADDED:
                folder_date_added = folder[item]
            elif item == preset.DATE_MODIFIED:
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
            elif item == preset.URL:
                folder_url = folder[item]
            else:
                tools.print_debug(preset.message['warning'] + str(item))
        folder_data = {
                'folder_info_guid': folder_guid,
                'folder_info_id': folder_id,
                'folder_info_sync_transaction_version': folder_sync_transaction_version,
                'folder_info_type': folder_type,
                'folder_info_date_added': utils.to_date(folder_date_added),
                'folder_info_date_modified': utils.to_date(folder_date_modified),
                'folder_info_last_visited': utils.to_date(folder_last_visited),
                'folder_info_name': folder_name,
                'folder_info_url': folder_url
        }
        for item in folder_item:
            folder_data_complete = folder_data | item
            data_header.append(folder_data_complete)
    return data_header
