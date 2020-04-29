import json
import tools
import public
import preset
import htmlSupport

from tools import add
from configparser import ConfigParser, DuplicateSectionError


@public.add
class Options:
    def __init__(self):
        self.export_file_type = False
        self.refresh_url_title = False
        self.remove_duplicated_urls = False
        self.remove_tracking_tokens_from_url = False
        self.import_urls_from_text_file = False
        self.refresh_folder_name_with_hostname_title = False

    '''
    @property
    def export_file_type(self):
        return self._export_file_type

    @export_file_type.setter
    def export_file_type(self, export_file_type):
        self._export_file_type = export_file_type

    @export_file_type.getter
    def export_file_type(self):
        return self._export_file_type

    @property
    def refresh_url_title(self):
        return self._refresh_url_title

    @refresh_url_title.setter
    def refresh_url_title(self, refresh_url_title):
        self._refresh_url_title = refresh_url_title

    @refresh_url_title.getter
    def refresh_url_title(self):
        return self._refresh_url_title

    @property
    def remove_duplicated_urls(self):
        return self._remove_duplicated_urls

    @remove_duplicated_urls.setter
    def remove_duplicated_urls(self, remove_duplicated_urls):
        self._remove_duplicated_urls = remove_duplicated_urls

    @remove_duplicated_urls.getter
    def remove_duplicated_urls(self):
        return self._remove_duplicated_urls

    @property
    def remove_tracking_tokens_from_url(self):
        return self._remove_tracking_tokens_from_url

    @remove_tracking_tokens_from_url.setter
    def remove_tracking_tokens_from_url(self, remove_tracking_tokens_from_url):
        self._remove_tracking_tokens_from_url = remove_tracking_tokens_from_url

    @remove_tracking_tokens_from_url.getter
    def remove_tracking_tokens_from_url(self):
        return self._remove_tracking_tokens_from_url

    @property
    def import_urls_from_text_file(self):
        return self._import_urls_from_text_file

    @import_urls_from_text_file.setter
    def import_urls_from_text_file(self, import_urls_from_text_file):
        self._import_urls_from_text_file = import_urls_from_text_file

    @import_urls_from_text_file.getter
    def import_urls_from_text_file(self):
        return self._import_urls_from_text_file

    @property
    def refresh_folder_name_with_hostname_title(self):
        return self._refresh_folder_name_with_hostname_title

    @refresh_folder_name_with_hostname_title.setter
    def refresh_folder_name_with_hostname_title(self, refresh_folder_name_with_hostname_title):
        self._refresh_folder_name_with_hostname_title = refresh_folder_name_with_hostname_title

    @refresh_folder_name_with_hostname_title.getter
    def refresh_folder_name_with_hostname_title(self):
        return self._refresh_folder_name_with_hostname_title
    '''

    def save_settings(self):
        category = 'main'
        config_file = 'config.ini'
        config = ConfigParser()
        config.read(config_file)
        try:
            config.add_section(category)
        except DuplicateSectionError:
            pass

        config.set(category, "export_file_type", str(self.export_file_type))
        config.set(category, "refresh_url_title", str(self.refresh_url_title))
        config.set(category, "remove_duplicated_urls", str(self.remove_duplicated_urls))
        config.set(category, "remove_tracking_tokens_from_url", str(self.remove_tracking_tokens_from_url))
        config.set(category, "import_urls_from_text_file", str(self.import_urls_from_text_file))
        config.set(category, "refresh_folder_name_with_hostname_title", str(self.refresh_folder_name_with_hostname_title))
        with open(config_file, 'w') as f:
            config.write(f)

    def load_settings(self):
        category = 'main'
        config_file = 'config.ini'
        config = ConfigParser()
        try:
            config.read(config_file)
            self.export_file_type = config.getboolean(category, "export_file_type")
            self.refresh_url_title = config.getboolean(category, "refresh_url_title")
            self.remove_duplicated_urls = config.getboolean(category, "remove_duplicated_urls")
            self.remove_tracking_tokens_from_url = config.getboolean(category, "remove_tracking_tokens_from_url")
            self.import_urls_from_text_file = config.getboolean(category, "import_urls_from_text_file")
            self.refresh_folder_name_with_hostname_title = config.getboolean(category, "refresh_folder_name_with_hostname_title")
        except Exception:
            self.export_file_type = False
            self.refresh_url_title = False
            self.remove_duplicated_urls = False
            self.remove_tracking_tokens_from_url = False
            self.import_urls_from_text_file = False
            self.refresh_folder_name_with_hostname_title = False


@public.add
class TemporaryObject:
    def __init__(self, element):
        index = [-1]
        self.date_added = element[add(index)]
        self.date_modified = element[add(index)]
        self.date_visited = element[add(index)]
        self.folder_name = element[add(index)]
        self.url_name = element[add(index)]
        self.url_clean = element[add(index)]
        self.original_url = element[add(index)]
        self.url_hostname = element[add(index)]

    def save(self):
        pass


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
        return tools.date_from_webkit(self["date_added"])

    @property
    def modified(self):
        if "date_modified" in self:
            return tools.date_from_webkit(self["date_modified"])

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


def read_content(content):
    data = []
    for chrome_url in content:
        date_added = '[Empty]'
        date_modified = '[Empty]'
        guid = '[Empty]'
        item_id = '[Empty]'
        last_visited = '[Empty]'
        name = '[Empty]'
        sync_transaction_version = '[Empty]'
        item_type = '[Empty]'
        url = '[Empty]'
        icon = '[Empty]'
        for x in chrome_url:
            if x == 'children':
                read_content(chrome_url[x])
            elif x == 'meta_info':
                for y in chrome_url[x]:
                    if y == 'last_visited':
                        last_visited = chrome_url[x][y]
            elif x == 'date_added':
                date_added = chrome_url[x]
            elif x == 'date_modified':
                date_modified = chrome_url[x]
            elif x == 'guid':
                guid = chrome_url[x]
            elif x == 'icon':
                #######################################################################################
                # TODO: Add icon to the spreadsheet
                #######################################################################################
                icon = chrome_url[x]
            elif x == 'id':
                item_id = chrome_url[x]
            elif x == 'name':
                name = chrome_url[x]
            elif x == 'sync_transaction_version':
                sync_transaction_version = chrome_url[x]
            elif x == 'type':
                item_type = chrome_url[x]
            elif x == 'url':
                url = chrome_url[x]
            else:
                tools.debug('WARNING: '+str(x))
        part1 = (
                 guid,
                 tools.to_number(item_id),
                 tools.to_number(sync_transaction_version),
                 item_type,

                 tools.to_date(date_added),
                 tools.to_date(date_modified),
                 tools.to_date(last_visited),

                 name,
                 htmlSupport.clean_url(url),
                 url
                )
        part2 = htmlSupport.parse_url(url)
        part3 = part1 + part2
        data.append(part3)
    return data


def generate_bookmarks(profile_):
    tools.display("Generating bookmarks...")
    bookmarks_file = preset.get_chrome_element(profile_, "Bookmarks")
    if bookmarks_file:
        return Bookmarks(bookmarks_file)
    return None


def generate_data(instance):
    for folder in instance.folders:
        data = None
        f_date_added = '[Empty]'
        f_date_modified = '[Empty]'
        f_guid = '[Empty]'
        f_id = '[Empty]'
        f_last_visited = '[Empty]'
        f_name = '[Empty]'
        f_sync_transaction_version = '[Empty]'
        f_type = '[Empty]'
        f_url = '[Empty]'
        for x in folder:
            if x == 'children':
                data = read_content(folder[x])
            elif x == 'meta_info':
                for y in folder[x]:
                    if y == 'last_visited':
                        f_last_visited = folder[x][y]
            elif x == 'date_added':
                f_date_added = folder[x]
            elif x == 'date_modified':
                f_date_modified = folder[x]
            elif x == 'guid':
                f_guid = folder[x]
            elif x == 'id':
                f_id = folder[x]
            elif x == 'name':
                f_name = folder[x]
            elif x == 'sync_transaction_version':
                f_sync_transaction_version = folder[x]
            elif x == 'type':
                f_type = folder[x]
            elif x == 'url':
                f_url = folder[x]
            else:
                tools.debug('WARNING: ' + str(x))
        f_data = (
                    f_guid,
                    tools.to_number(f_id),
                    tools.to_number(f_sync_transaction_version),
                    f_type,

                    tools.to_date(f_date_added),
                    tools.to_date(f_date_modified),
                    tools.to_date(f_last_visited),

                    f_name,
                    f_url
                 )

        for d in data:
            new_data = f_data + d
            preset.data_header.append(new_data)
    return preset.data_header
