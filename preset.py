import utils
from json import load
from pathlib import Path

main_icon = 'resources/blue.ico'
configuration_filename = 'resources/config.ini'
translation_filename = 'resources/translation.json'


def add_value(value):
    value[0] = value[0] + 1
    return value[0]


def load_translation_file():
    return load(Path(translation_filename).open(encoding=UTF8))


def read_tokens(category):
    cat_list = []
    with open('tokens.txt', 'r', encoding=UTF8) as tks:
        lines = tks.readlines()
        for line in lines:
            if line.startswith(category):
                cat_list.append(line.split('|')[1].strip())
    return cat_list


RUN_GUI = False

MAIN_SECTION = 'main'

DATABASE_URL = 'mongodb://localhost:27017/'
DATABASE_NAME = 'ChromeBookMarks'
DATABASE_COLLECTION = 'BookMarksLinks'
DATABASE_COLLECTION_NAMES = 'BookMarksNames'
DATABASE_COLLECTION_FOLDERS = 'BookMarksFolders'

DEBUG_MODE = False
TEXT_FILENAME = 'chrome.txt'
HTML_FILENAME = 'chrome.html'
XLSX_FILENAME = 'chrome.xlsx'

TXT = 'txt'
HTML = 'html'
XLSX = 'xlsx'
UTF8 = 'UTF8'
LATIN = 'latin1'
TITLE = 'title'
ENABLED = 'enabled'
DISABLED = 'disabled'

YOUTUBE_WWW = 'www.youtube.com'
YOUTUBE_M = 'm.youtube.com'
YOUTUBE_COM = 'youtube.com'
YOUTUBE = 'youtu.be'
FACEBOOK_COM = 'facebook.com'

ENGLISH = 'en-us'
message = load_translation_file()[ENGLISH]

TIMEOUT = 5

ON = 'on'
OFF = 'off'
NONE = None
TRUE = True
FALSE = False
EMPTY = ''
BLANK = ' '
PROFILES = 'all'

PROTOCOL = 'http://'

PREFERENCES = 'Preferences'
BOOKMARKS = 'Bookmarks'
UNKNOWN = 'unknown_exception'

TAB = '\t'
NEW_LINE = '\n'
RECURSE = '\r'
FORWARD_SLASHES = '//'

NO_TITLE = '[NO_TITLE]'

QUOTE = "'"
UNDERLINE = '_'
OVERLINE = '‾'

NO_HOST_NAME = '[no hostname]'
NO_SITE_NAME = '[no site name]'
NO_CLEAN_url = '[no clean url]'
NO_url_ADDRESS = '[no url address]'

CHILDREN = 'children'
META_INFO = 'meta_info'
LAST_VISITED = 'last_visited'
DATE_ADDED = 'date_added'
DATE_MODIFIED = 'date_modified'
GUID = 'guid'
ICON = 'icon'
ITEM_ID = 'id'
ITEM_NAME = 'name'
SYNC_TRANSACTION_VERSION = 'sync_transaction_version'
ITEM_TYPE = 'type'
URL = 'url'

NONAME = 'NONAME'

NO_DATE = 'no_date'
EMPTY_STRING = 'empty'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
NUMBER_FORMAT = 'YYYY/MM/DD hh:mm:ss'

DEBUG_SYSTEM = 'debug_system'
LOAD_TIME_OUT = 'load_time_out'
system_language = 'system_language'
export_file_type = 'export_file_type'
refresh_url_title = 'refresh_url_title'
exit_dialog_confirmation = 'exit_confirmation'
remove_duplicated_urls = 'remove_duplicated_urls'
remove_tracking_tokens_from_url = 'remove_tracking_tokens_from_url'
display_exit_dialog = 'display_exit_dialog'
refresh_folder_name_with_hostname_title = 'refresh_folder_name_with_hostname_title'

SYMBOLS = ['?', '#', '&']

dict_params = {
            'facebook.com': read_tokens('facebook'),
            'folha.uol': read_tokens('folha'),
            'general': read_tokens('general'),
            'globo.com': read_tokens('globo'),
            'instagram': read_tokens('instagram'),
            'magazineluiza.com.br': read_tokens('magazine'),
            'mercadolivre.com': read_tokens('mercadolivre'),
            'mercadoshops.com': read_tokens('mercadoshops'),
            'minds.com': read_tokens('minds'),
            'savefrom.net': read_tokens('savefrom'),
            'submarino.com': read_tokens('submarino'),
            'tracking_module': read_tokens('tracking_module'),
            'uol': read_tokens('uol'),
            'youtube.com': read_tokens('youtube')
          }

cli_progress_dialog = None
gui_progress_dialog = None


def set_language(selected_language):
    global message
    message = load_translation_file()[selected_language]


def get_languages():
    language_list = []
    for language_item in load_translation_file():
        language_list.append(language_item)
    return language_list


folder_guid_attr = 'folder_guid'
folder_id_attr = 'folder_id'
folder_sync_attr = 'folder_sync'
folder_type_attr = 'folder_type'

folder_added_attr = 'folder_added'
folder_modified_attr = 'folder_modified'
folder_visited_attr = 'folder_visited'

folder_name_attr = 'folder_name'
folder_url_attr = 'folder_url'

url_guid_attr = 'url_guid'
url_id_attr = 'url_id'
url_sync_attr = 'url_sync'
url_type_attr = 'url_type'

url_added_attr = 'url_added'
url_modified_attr = 'url_modified'
url_visited_attr = 'url_visited'

url_name_attr = 'url_name'
url_clean_attr = 'url_clean'
url_attr = 'url'
scheme_attr = 'scheme'
netloc_attr = 'netloc'
hostname_attr = 'hostname'
path_attr = 'path'
port_attr = 'port'
param_attr = 'param'
fragment_attr = 'fragment'
username_attr = 'username'
password_attr = 'password'

param_a_attr = 'param_a'
param_b_attr = 'param_b'
param_c_attr = 'param_c'
param_d_attr = 'param_d'
param_e_attr = 'param_e'
param_f_attr = 'param_f'
param_g_attr = 'param_g'
param_h_attr = 'param_h'
param_i_attr = 'param_i'
param_j_attr = 'param_j'
param_k_attr = 'param_k'
param_l_attr = 'param_l'
param_m_attr = 'param_m'
param_n_attr = 'param_n'
param_o_attr = 'param_o'
param_p_attr = 'param_p'


class Header:
    def __init__(self):
        index = [-1]
        stub_date = utils.to_date(13231709218000000)

        self._folder_guid = (EMPTY, add_value(index))
        self._folder_id = (EMPTY, add_value(index))
        self._folder_sync = (EMPTY, add_value(index))
        self._folder_type = (EMPTY, add_value(index))

        self._folder_added = (stub_date, add_value(index))
        self._folder_modified = (stub_date, add_value(index))
        self._folder_visited = (stub_date, add_value(index))

        self._folder_name = (EMPTY, add_value(index))
        self._folder_url = (EMPTY, add_value(index))

        self._url_guid = (EMPTY, add_value(index))
        self._url_id = (EMPTY, add_value(index))
        self._url_sync = (EMPTY, add_value(index))
        self._url_type = (EMPTY, add_value(index))

        self._url_added = (stub_date, add_value(index))
        self._url_modified = (stub_date, add_value(index))
        self._url_visited = (stub_date, add_value(index))

        self._url_name = (NO_SITE_NAME, add_value(index))
        self._url_clean = (NO_CLEAN_url, add_value(index))
        self._url = (NO_url_ADDRESS, add_value(index))
        self._icon = (EMPTY, add_value(index))
        self._scheme = (EMPTY, add_value(index))
        self._netloc = (EMPTY, add_value(index))
        self._hostname = (NO_HOST_NAME, add_value(index))
        self._path = (EMPTY, add_value(index))
        self._port = (EMPTY, add_value(index))
        self._param = (EMPTY, add_value(index))
        self._fragment = (EMPTY, add_value(index))
        self._username = (EMPTY, add_value(index))
        self._password = (EMPTY, add_value(index))

        self._param_a = (EMPTY, add_value(index))
        self._param_b = (EMPTY, add_value(index))
        self._param_c = (EMPTY, add_value(index))
        self._param_d = (EMPTY, add_value(index))
        self._param_e = (EMPTY, add_value(index))
        self._param_f = (EMPTY, add_value(index))
        self._param_g = (EMPTY, add_value(index))
        self._param_h = (EMPTY, add_value(index))
        self._param_i = (EMPTY, add_value(index))
        self._param_j = (EMPTY, add_value(index))
        self._param_k = (EMPTY, add_value(index))
        self._param_l = (EMPTY, add_value(index))
        self._param_m = (EMPTY, add_value(index))
        self._param_n = (EMPTY, add_value(index))
        self._param_o = (EMPTY, add_value(index))
        self._param_p = (EMPTY, add_value(index))

    def set_data(self, url_element):
        index = [-1]

        self._folder_guid = (url_element[add_value(index)], index[0])
        self._folder_id = (url_element[add_value(index)], index[0])
        self._folder_sync = (url_element[add_value(index)], index[0])
        self._folder_type = (url_element[add_value(index)], index[0])

        self._folder_added = (url_element[add_value(index)], index[0])
        self._folder_modified = (url_element[add_value(index)], index[0])
        self._folder_visited = (url_element[add_value(index)], index[0])

        self._folder_name = (url_element[add_value(index)], index[0])
        self._folder_url = (url_element[add_value(index)], index[0])

        self._url_guid = (url_element[add_value(index)], index[0])
        self._url_id = (url_element[add_value(index)], index[0])
        self._url_sync = (url_element[add_value(index)], index[0])
        self._url_type = (url_element[add_value(index)], index[0])

        self._url_added = (url_element[add_value(index)], index[0])
        self._url_modified = (url_element[add_value(index)], index[0])
        self._url_visited = (url_element[add_value(index)], index[0])

        self._url_name = (url_element[add_value(index)], index[0])
        self._url_clean = (url_element[add_value(index)], index[0])
        self._url = (url_element[add_value(index)], index[0])
        self._icon = (url_element[add_value(index)], index[0])
        self._scheme = (url_element[add_value(index)], index[0])
        self._netloc = (url_element[add_value(index)], index[0])
        self._hostname = (url_element[add_value(index)], index[0])
        self._path = (url_element[add_value(index)], index[0])
        self._port = (url_element[add_value(index)], index[0])
        self._param = (url_element[add_value(index)], index[0])
        self._fragment = (url_element[add_value(index)], index[0])
        self._username = (url_element[add_value(index)], index[0])
        self._password = (url_element[add_value(index)], index[0])

        self._param_a = (url_element[add_value(index)], index[0])
        self._param_b = (url_element[add_value(index)], index[0])
        self._param_c = (url_element[add_value(index)], index[0])
        self._param_d = (url_element[add_value(index)], index[0])
        self._param_e = (url_element[add_value(index)], index[0])
        self._param_f = (url_element[add_value(index)], index[0])
        self._param_g = (url_element[add_value(index)], index[0])
        self._param_h = (url_element[add_value(index)], index[0])
        self._param_i = (url_element[add_value(index)], index[0])
        self._param_j = (url_element[add_value(index)], index[0])
        self._param_k = (url_element[add_value(index)], index[0])
        self._param_l = (url_element[add_value(index)], index[0])
        self._param_m = (url_element[add_value(index)], index[0])
        self._param_n = (url_element[add_value(index)], index[0])
        self._param_o = (url_element[add_value(index)], index[0])
        self._param_p = (url_element[add_value(index)], index[0])

    def get_position(self, index):
        item = self.to_tuple()
        return item[index]

    def get_name(self, name):
        item = self.to_dict()
        return item['_' + name]

    def to_list(self):
        dictionary = self.__dict__
        item_list = []
        for item in dictionary:
            item_list.append(dictionary[item])
        item_list.sort(key=lambda element: element[1])
        element_list = []
        for item in item_list:
            element_list.append(item[0])
        return element_list

    def to_dict(self):
        indexed_dictionary = self.__dict__
        dictionary = {}
        for element in indexed_dictionary:
            dictionary.update({element: indexed_dictionary[element][0]})
        return dictionary

    def to_tuple(self):
        dictionary = self.__dict__
        item_list = []
        for item in dictionary:
            item_list.append(dictionary[item])
        item_list.sort(key=lambda element: element[1])
        tuple_list = []
        for item in item_list:
            tuple_list.append(item[0])
        return tuple(tuple_list)

    @staticmethod
    def get_label(self, index):
        return label_dictionary[index]

    def to_dict_index(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)

    @property
    def folder_guid(self):
        return self._folder_guid

    @folder_guid.setter
    def folder_guid(self, folder_guid):
        self._folder_guid = (folder_guid, self._folder_guid[1])

    @folder_guid.getter
    def folder_guid(self):
        return self._folder_guid[0]

    @property
    def folder_id(self):
        return self._folder_id

    @folder_id.setter
    def folder_id(self, folder_id):
        self._folder_id = (folder_id, self._folder_id[1])

    @folder_id.getter
    def folder_id(self):
        return self._folder_id[0]

    @property
    def folder_sync(self):
        return self._folder_sync

    @folder_sync.setter
    def folder_sync(self, folder_sync):
        self._folder_sync = (folder_sync, self._folder_sync[1])

    @folder_sync.getter
    def folder_sync(self):
        return self._folder_sync[0]

    @property
    def folder_type(self):
        return self._folder_type

    @folder_type.setter
    def folder_type(self, folder_type):
        self._folder_type = (folder_type, self._folder_type[1])

    @folder_type.getter
    def folder_type(self):
        return self._folder_type[0]

    @property
    def folder_added(self):
        return self._folder_added

    @folder_added.setter
    def folder_added(self, folder_added):
        self._folder_added = (folder_added, self._folder_added[1])

    @folder_added.getter
    def folder_added(self):
        return self._folder_added[0]

    @property
    def folder_modified(self):
        return self._folder_modified

    @folder_modified.setter
    def folder_modified(self, folder_modified):
        self._folder_modified = (folder_modified, self._folder_modified[1])

    @folder_modified.getter
    def folder_modified(self):
        return self._folder_modified[0]

    @property
    def folder_visited(self):
        return self._folder_visited

    @folder_visited.setter
    def folder_visited(self, folder_visited):
        self._folder_visited = (folder_visited, self._folder_visited[1])

    @folder_visited.getter
    def folder_visited(self):
        return self._folder_visited[0]

    @property
    def folder_name(self):
        return self._folder_name

    @folder_name.setter
    def folder_name(self, folder_name):
        self._folder_name = (folder_name, self._folder_name[1])

    @folder_name.getter
    def folder_name(self):
        return self._folder_name[0]

    @property
    def folder_url(self):
        return self._folder_url

    @folder_url.setter
    def folder_url(self, folder_url):
        self._folder_url = (folder_url, self._folder_url[1])

    @folder_url.getter
    def folder_url(self):
        return self._folder_url[0]

    @property
    def url_guid(self):
        return self._url_guid

    @url_guid.setter
    def url_guid(self, url_guid):
        self._url_guid = (url_guid, self._url_guid[1])

    @url_guid.getter
    def url_guid(self):
        return self._url_guid[0]

    @property
    def url_id(self):
        return self._url_id

    @url_id.setter
    def url_id(self, url_id):
        self._url_id = (url_id, self._url_id[1])

    @url_id.getter
    def url_id(self):
        return self._url_id[0]

    @property
    def url_sync(self):
        return self._url_sync

    @url_sync.setter
    def url_sync(self, url_sync):
        self._url_sync = (url_sync, self._url_sync[1])

    @url_sync.getter
    def url_sync(self):
        return self._url_sync[0]

    @property
    def url_type(self):
        return self._url_type

    @url_type.setter
    def url_type(self, url_type):
        self._url_type = (url_type, self._url_type[1])

    @url_type.getter
    def url_type(self):
        return self._url_type[0]

    @property
    def url_added(self):
        return self._url_added

    @url_added.setter
    def url_added(self, url_added):
        self._url_added = (url_added, self._url_added[1])

    @url_added.getter
    def url_added(self):
        return self._url_added[0]

    @property
    def url_modified(self):
        return self._url_modified

    @url_modified.setter
    def url_modified(self, url_modified):
        self._url_modified = (url_modified, self._url_modified[1])

    @url_modified.getter
    def url_modified(self):
        return self._url_modified[0]

    @property
    def url_visited(self):
        return self._url_visited

    @url_visited.setter
    def url_visited(self, url_visited):
        self._url_visited = (url_visited, self._url_visited[1])

    @url_visited.getter
    def url_visited(self):
        return self._url_visited[0]

    @property
    def url_name(self):
        return self._url_name

    @url_name.setter
    def url_name(self, url_name):
        self._url_name = (url_name, self._url_name[1])

    @url_name.getter
    def url_name(self):
        return self._url_name[0]

    @property
    def url_clean(self):
        return self._url_clean

    @url_clean.setter
    def url_clean(self, url_clean):
        self._url_clean = (url_clean, self._url_clean[1])

    @url_clean.getter
    def url_clean(self):
        return self._url_clean[0]

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, yurl):
        self._url = (yurl, self._url[1])

    @url.getter
    def url(self):
        return self._url[0]

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, y_icon):
        self._icon = (y_icon, self._icon[1])

    @icon.getter
    def icon(self):
        return self._icon[0]

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme):
        self._scheme = (scheme, self._scheme[1])

    @scheme.getter
    def scheme(self):
        return self._scheme[0]

    @property
    def netloc(self):
        return self._netloc

    @netloc.setter
    def netloc(self, netloc):
        self._netloc = (netloc, self._netloc[1])

    @netloc.getter
    def netloc(self):
        return self._netloc[0]

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        self._hostname = (hostname, self._hostname[1])

    @hostname.getter
    def hostname(self):
        return self._hostname[0]

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = (path, self._path[1])

    @path.getter
    def path(self):
        return self._path[0]

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = (port, self._port[1])

    @port.getter
    def port(self):
        return self._port[0]

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, param):
        self._param = (param, self._param[1])

    @param.getter
    def param(self):
        return self._param[0]

    @property
    def fragment(self):
        return self._fragment

    @fragment.setter
    def fragment(self, fragment):
        self._fragment = (fragment, self._fragment[1])

    @fragment.getter
    def fragment(self):
        return self._fragment[0]

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, user_name):
        self._username = (user_name, self._username[1])

    @username.getter
    def username(self):
        return self._username[0]

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, user_password):
        self._password = (user_password, self._password[1])

    @password.getter
    def password(self):
        return self._password[0]

    @property
    def param_a(self):
        return self._param_a

    @param_a.setter
    def param_a(self, a_param):
        self._param_a = (a_param, self._param_a[1])

    @param_a.getter
    def param_a(self):
        return self._param_a[0]

    @property
    def param_b(self):
        return self._param_b

    @param_b.setter
    def param_b(self, b_param):
        self._param_b = (b_param, self._param_b[1])

    @param_b.getter
    def param_b(self):
        return self._param_b[0]

    @property
    def param_c(self):
        return self._param_c

    @param_c.setter
    def param_c(self, c_param):
        self._param_c = (c_param, self._param_c[1])

    @param_c.getter
    def param_c(self):
        return self._param_c[0]

    @property
    def param_d(self):
        return self._param_d

    @param_d.setter
    def param_d(self, d_param):
        self._param_d = (d_param, self._param_d[1])

    @param_d.getter
    def param_d(self):
        return self._param_d[0]

    @property
    def param_e(self):
        return self._param_e

    @param_e.setter
    def param_e(self, e_param):
        self._param_e = (e_param, self._param_e[1])

    @param_e.getter
    def param_e(self):
        return self._param_e[0]

    @property
    def param_f(self):
        return self._param_f

    @param_f.setter
    def param_f(self, f_param):
        self._param_f = (f_param, self._param_f[1])

    @param_f.getter
    def param_f(self):
        return self._param_f[0]

    @property
    def param_g(self):
        return self._param_g

    @param_g.setter
    def param_g(self, g_param):
        self._param_g = (g_param, self._param_g[1])

    @param_g.getter
    def param_g(self):
        return self._param_g[0]

    @property
    def param_h(self):
        return self._param_h

    @param_h.setter
    def param_h(self, h_param):
        self._param_h = (h_param, self._param_h[1])

    @param_h.getter
    def param_h(self):
        return self._param_h[0]

    @property
    def param_i(self):
        return self._param_i

    @param_i.setter
    def param_i(self, i_param):
        self._param_i = (i_param, self._param_i[1])

    @param_i.getter
    def param_i(self):
        return self._param_i[0]

    @property
    def param_j(self):
        return self._param_j

    @param_j.setter
    def param_j(self, j_param):
        self._param_j = (j_param, self._param_j[1])

    @param_j.getter
    def param_j(self):
        return self._param_j[0]

    @property
    def param_k(self):
        return self._param_k

    @param_k.setter
    def param_k(self, k_param):
        self._param_k = (k_param, self._param_k[1])

    @param_k.getter
    def param_k(self):
        return self._param_k[0]

    @property
    def param_l(self):
        return self._param_l

    @param_l.setter
    def param_l(self, l_param):
        self._param_l = (l_param, self._param_l[1])

    @param_l.getter
    def param_l(self):
        return self._param_l[0]

    @property
    def param_m(self):
        return self._param_m

    @param_m.setter
    def param_m(self, m_param):
        self._param_m = (m_param, self._param_m[1])

    @param_m.getter
    def param_m(self):
        return self._param_m[0]

    @property
    def param_n(self):
        return self._param_n

    @param_n.setter
    def param_n(self, n_param):
        self._param_n = (n_param, self._param_n[1])

    @param_n.getter
    def param_n(self):
        return self._param_n[0]

    @property
    def param_o(self):
        return self._param_o

    @param_o.setter
    def param_o(self, o_param):
        self._param_o = (o_param, self._param_o[1])

    @param_o.getter
    def param_o(self):
        return self._param_o[0]

    @property
    def param_p(self):
        return self._param_p

    @param_p.setter
    def param_p(self, p_param):
        self._param_p = (p_param, self._param_p[1])

    @param_p.getter
    def param_p(self):
        return self._param_p[0]


position = [-1]
label_dictionary = {
                    str(add_value(position)): 'Folder GUID',
                    str(add_value(position)): 'Folder ID',
                    str(add_value(position)): 'Folder Sync',
                    str(add_value(position)): 'Type',

                    str(add_value(position)): 'Folder Added',
                    str(add_value(position)): 'Folder Modified',
                    str(add_value(position)): 'Folder visited',

                    str(add_value(position)): 'Folder Name',
                    str(add_value(position)): 'Folder url',

                    str(add_value(position)): 'url GUID',
                    str(add_value(position)): 'url ID',
                    str(add_value(position)): 'url Sync',
                    str(add_value(position)): 'Type',

                    str(add_value(position)): 'url Added',
                    str(add_value(position)): 'url Modified',
                    str(add_value(position)): 'url Visited',

                    str(add_value(position)): 'url Name',
                    str(add_value(position)): 'url Clean',
                    str(add_value(position)): 'url',
                    str(add_value(position)): 'icon',

                    str(add_value(position)): 'scheme',
                    str(add_value(position)): 'netloc',
                    str(add_value(position)): 'hostname',
                    str(add_value(position)): 'path',
                    str(add_value(position)): 'port',
                    str(add_value(position)): 'param',
                    str(add_value(position)): 'fragment',
                    str(add_value(position)): 'username',
                    str(add_value(position)): 'password',

                    str(add_value(position)): 'param_a',
                    str(add_value(position)): 'param_b',
                    str(add_value(position)): 'param_c',
                    str(add_value(position)): 'param_d',
                    str(add_value(position)): 'param_e',
                    str(add_value(position)): 'param_f',
                    str(add_value(position)): 'param_g',
                    str(add_value(position)): 'param_h',
                    str(add_value(position)): 'param_i',
                    str(add_value(position)): 'param_j',
                    str(add_value(position)): 'param_k',
                    str(add_value(position)): 'param_l',
                    str(add_value(position)): 'param_m',
                    str(add_value(position)): 'param_n',
                    str(add_value(position)): 'param_o',
                    str(add_value(position)): 'param_p'
    }

TRAIL = (
    BLANK,  # 29
    BLANK,  # 30
    BLANK,  # 31
    BLANK,  # 32
    BLANK,  # 33
    BLANK,  # 34
    BLANK,  # 35
    BLANK,  # 36
    BLANK,  # 37
    BLANK,  # 38
    BLANK,  # 39
    BLANK,  # 40
    BLANK,  # 41
    BLANK,  # 42
    BLANK,  # 43
    BLANK   # 44
        )
