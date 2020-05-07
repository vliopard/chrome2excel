import json
import tools
import utils
import public
import preset
import htmlSupport

from configparser import ConfigParser, DuplicateSectionError


@public.add
class Options:
    def __init__(self):
        self.system_language = preset.english
        self.debug_system = False
        self.export_file_type = False
        self.refresh_url_title = False
        self.remove_duplicated_urls = False
        self.remove_tracking_tokens_from_url = False
        self.import_urls_from_text_file = False
        self.refresh_folder_name_with_hostname_title = False

        self.configuration_category = preset.main_section
        self.configuration_parser = ConfigParser()
        self.configuration_parser.read(preset.configuration_filename)

    def save_settings(self):
        try:
            self.configuration_parser.add_section(self.configuration_category)
        except DuplicateSectionError:
            pass

        self.configuration_parser.set(self.configuration_category, preset.debug_system, str(preset.debug_mode))
        self.configuration_parser.set(self.configuration_category, preset.load_time_out, str(preset.timeout))
        self.configuration_parser.set(self.configuration_category, preset.system_language, str(self.system_language))
        self.configuration_parser.set(self.configuration_category, preset.export_file_type, str(self.export_file_type))
        self.configuration_parser.set(self.configuration_category, preset.refresh_url_title, str(self.refresh_url_title))
        self.configuration_parser.set(self.configuration_category, preset.remove_duplicated_urls, str(self.remove_duplicated_urls))
        self.configuration_parser.set(self.configuration_category, preset.remove_tracking_tokens_from_url, str(self.remove_tracking_tokens_from_url))
        self.configuration_parser.set(self.configuration_category, preset.import_urls_from_text_file, str(self.import_urls_from_text_file))
        self.configuration_parser.set(self.configuration_category, preset.refresh_folder_name_with_hostname_title, str(self.refresh_folder_name_with_hostname_title))
        with open(preset.configuration_filename, 'w') as configuration_file:
            self.configuration_parser.write(configuration_file)

    def load_settings(self):
        try:
            preset.debug_mode = self.configuration_parser.getboolean(self.configuration_category, preset.debug_system)
            preset.timeout = self.configuration_parser.getint(self.configuration_category, preset.load_time_out)
            self.system_language = self.configuration_parser.get(self.configuration_category, preset.system_language)
            self.export_file_type = self.configuration_parser.getboolean(self.configuration_category, preset.export_file_type)
            self.refresh_url_title = self.configuration_parser.getboolean(self.configuration_category, preset.refresh_url_title)
            self.remove_duplicated_urls = self.configuration_parser.getboolean(self.configuration_category, preset.remove_duplicated_urls)
            self.remove_tracking_tokens_from_url = self.configuration_parser.getboolean(self.configuration_category, preset.remove_tracking_tokens_from_url)
            self.import_urls_from_text_file = self.configuration_parser.getboolean(self.configuration_category, preset.import_urls_from_text_file)
            self.refresh_folder_name_with_hostname_title = self.configuration_parser.getboolean(self.configuration_category, preset.refresh_folder_name_with_hostname_title)
        except Exception:
            preset.timeout = 120
            preset.debug_mode = False
            self.system_language = preset.english
            self.export_file_type = False
            self.refresh_url_title = False
            self.remove_duplicated_urls = False
            self.remove_tracking_tokens_from_url = False
            self.import_urls_from_text_file = False
            self.refresh_folder_name_with_hostname_title = False
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
        self.data = json.loads(open(path, encoding='utf-8').read())
        self.attrList = self.processRoots()
        self.urls = self.attrList["urls"]
        self.folders = self.attrList["folders"]

    def processRoots(self):
        attribute_list = {"urls": [], "folders": []}
        for key, value in json.loads(open(self.path, encoding='utf-8').read())["roots"].items():
            if "children" in value:
                self.processTree(attribute_list, value["children"])
        return attribute_list

    def processTree(self, attribute_list, children_list):
        for item in children_list:
            self.processUrls(item, attribute_list, children_list)
            self.processFolders(item, attribute_list, children_list)

    def processUrls(self, item, attribute_list, children_list):
        if "type" in item and item["type"] == "url":
            attribute_list["urls"].append(Item(item))

    def processFolders(self, item, attribute_list, children_list):
        if "type" in item and item["type"] == "folder":
            attribute_list["folders"].append(Item(item))
            if "children" in item:
                self.processTree(attribute_list, item["children"])


def read_content(folder_items):
    url_list = []
    for folder_item in folder_items:
        url_date_added = preset.empty
        url_date_modified = preset.empty
        url_guid = preset.empty
        url_item_id = preset.empty
        url_last_visited = preset.empty
        url_name = preset.empty
        url_sync_transaction_version = preset.empty
        url_item_type = preset.empty
        url_address = preset.empty
        url_icon = preset.empty
        for item in folder_item:
            if item == preset.children:
                read_content(folder_item[item])
            elif item == preset.meta_info:
                for element in folder_item[item]:
                    if element == preset.last_visited:
                        url_last_visited = folder_item[item][element]
            elif item == preset.date_added:
                url_date_added = folder_item[item]
            elif item == preset.date_modified:
                url_date_modified = folder_item[item]
            elif item == preset.guid:
                url_guid = folder_item[item]
            elif item == preset.icon:
                url_icon = folder_item[item]
            elif item == preset.item_id:
                url_item_id = folder_item[item]
            elif item == preset.item_name:
                url_name = folder_item[item]
            elif item == preset.sync_transaction_version:
                url_sync_transaction_version = folder_item[item]
            elif item == preset.item_type:
                url_item_type = folder_item[item]
            elif item == preset.url:
                url_address = folder_item[item]
            else:
                tools.debug(preset.message["warning"] + str(item))
        url_data = (
                url_guid,
                utils.to_number(url_item_id),
                utils.to_number(url_sync_transaction_version),
                url_item_type,

                utils.to_date(url_date_added),
                utils.to_date(url_date_modified),
                utils.to_date(url_last_visited),

                url_name,
                htmlSupport.clean_url(url_address),
                url_address,
                url_icon
        )
        parsed_url = htmlSupport.parse_url(url_address)
        url_list.append(url_data + parsed_url)
    return url_list


def generate_bookmarks(profile):
    tools.display(preset.message["generating_bookmarks"])
    bookmarks_file = tools.get_chrome_element(profile, preset.bookmarks)
    if bookmarks_file:
        return Bookmarks(bookmarks_file)
    return None


def generate_data(instance):
    data_header = []

    for folder in instance.folders:

        folder_item = None
        folder_date_added = preset.no_date
        folder_date_modified = preset.no_date
        folder_guid = preset.empty
        folder_id = preset.empty
        folder_last_visited = preset.no_date
        folder_name = preset.empty
        folder_sync_transaction_version = preset.empty
        folder_type = preset.empty
        folder_url = preset.empty

        for item in folder:
            if item == preset.children:
                folder_item = read_content(folder[item])
            elif item == preset.meta_info:
                for element in folder[item]:
                    if element == preset.last_visited:
                        folder_last_visited = folder[item][element]
            elif item == preset.date_added:
                folder_date_added = folder[item]
            elif item == preset.date_modified:
                folder_date_modified = folder[item]
            elif item == preset.guid:
                folder_guid = folder[item]
            elif item == preset.item_id:
                folder_id = folder[item]
            elif item == preset.item_name:
                folder_name = folder[item]
            elif item == preset.sync_transaction_version:
                folder_sync_transaction_version = folder[item]
            elif item == preset.item_type:
                folder_type = folder[item]
            elif item == preset.url:
                folder_url = folder[item]
            else:
                tools.debug(preset.message["warning"] + str(item))

        folder_data = (
                folder_guid,
                utils.to_number(folder_id),
                utils.to_number(folder_sync_transaction_version),
                folder_type,

                utils.to_date(folder_date_added),
                utils.to_date(folder_date_modified),
                utils.to_date(folder_last_visited),

                folder_name,
                folder_url
        )
        for item in folder_item:
            data_header.append(folder_data + item + preset.trail)
    return data_header
