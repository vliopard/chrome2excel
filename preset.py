import utils
import screen
import configparser
from json import load
from pathlib import Path

ABOUT = 'about'
ABOUT_DESCRIPTION = 'about_description'
ABOUT_MENU = 'about_menu'
ACCEPT = 'Accept'
ACCEPT_ENCODING = 'Accept-Encoding'
ACCEPT_LANGUAGE = 'Accept-Language'
ACCOUNT_INFO = 'account_info'
ALL_PROFILES = 'all_profiles'
APPENDING_DATA_TABLE = 'appending_data_table'
APPLICATION_DESCRIPTION = 'application_description'
APPLICATION_LICENCE = 'application_licence'
APPLICATION_TITLE = 'application_title'
APPLICATION_WEBSITE = 'application_website'
ARCHIVE_FTP = 'Archive (FTP)'
ARCHIVE_IMG = 'Archive (IMG)'
ARCHIVE_JAVASCRIPT = 'Archive (JavaScript)'
ARCHIVE_MP4 = 'Archive (MP4)'
ARCHIVE_PDF = 'Archive (PDF)'
ARCHIVE_PRG = 'Archive (PRG)'
ARCHIVE_SRC = 'Archive (SRC)'
ARCHIVE_ZIP = 'Archive (ZIP)'
BOOKMARKS = 'Bookmarks'
BOOKMARKS_CHILDREN = 'children'
BOOKMARKS_EDITOR = 'bookmarks_editor'
BOOKMARKS_FOLDER = 'folder'
BOOKMARKS_FOLDERS = 'folders'
BOOKMARKS_ROOTS = 'roots'
BOOKMARKS_TYPE = 'type'
BOOKMARKS_URL = 'url'
BOOKMARKS_URLS = 'urls'
CANCEL_BUTTON = 'cancel_button'
CHARSET = 'charset'
CHARSET_ASCII = 'ASCII'
CHARSET_EQ = 'charset='
CHARSET_ISO88591 = 'ISO-8859-1'
CHARSET_JOHAB = 'Johab'
CHARSET_LATIN = 'latin1'
CHARSET_LATIN1 = 'Latin-1'
CHARSET_MACROMAN = 'MacRoman'
CHARSET_UTF8 = 'UTF-8'
CHARSET_WINDOWS1251 = 'Windows-1251'
CHARSET_WINDOWS1254 = 'windows-1254'
CHARSET_WINDOWS1256 = 'windows-1256'
CHECK_HOSTNAME = 'check_hostname'
CHOOSE_FILE = 'choose_file'
CHROME = 'chrome'
CHROMESETTINGS = 'ChromeSettings'
CHROME_EXPORTER = 'Chrome Exporter'
CHROME_SETTINGS = 'Chrome Settings'
CHROME_URLS = 'chrome_urls'
COMMAND_CLEAN_URL_FROM_TRACKING = 'clean'
CLEAN_URL_BOOL = False
CLEAN_URL_STRING = 'clean_url'
CLI_PROGRESS_DIALOG = None
PROGRESS_BAR_DISABLED = True
COLUMNS = 'COLUMNS'

CONFIGURATION_FILENAME = 'resources/config.ini'
config = configparser.ConfigParser()
config.read(CONFIGURATION_FILENAME)

CONTENT = 'content'
CONTENT_TYPE = 'content-type'
DATABASE_COLLECTION = 'BookMarksLinks'
DATABASE_COLLECTION_FOLDERS = 'BookMarksFolders'
DATABASE_COLLECTION_NAMES = 'BookMarksNames'
DATABASE_STATUS = 'BookMarksStatus'
DATABASE_ID = '_id'
DATABASE_NAME = 'ChromeBookMarks'

MONGO_HOST = config.get('security', 'HOST')
MONGO_PORT = config.get('security', 'PORT')
try:
    MONGO_USERNAME = config.get('security', 'USERNAME')
except Exception as exception:
    MONGO_USERNAME = ''

if not MONGO_USERNAME:
    DATABASE_URL = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/'
else:
    MONGO_PASSWORD = config.get('security', 'PASSWORD')
    if not MONGO_PASSWORD:
        MONGO_PASSWORD = input('Enter database password: ')
    DATABASE_URL = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/'

DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
DEBUG_MODE = False
DEBUG_SYSTEM = 'debug_system'
DEFAULT_L = 'default'
DIRECTORY_SUGGESTION = False
DISABLED = 'disabled'
DISPLAY_EXIT_DIALOG = 'display_exit_dialog'
DONE = 'done'
DTOKEN = 'D['
DUPE = 'DUPE'
EDIT = 'edit'
EDIT_SAVE = 'edit_save'
EDIT_TITLE = 'edit_title'
EMAIL = 'email'
EMPTY_STRING = 'empty'
ENABLED = 'enabled'
ENCODING = 'encoding'
ENGLISH = 'en-us'
ERROR = 'Error'
EXIT_CONFIRMATION = 'exit_confirmation'
EXIT_DESCRIPTION = 'exit_description'
EXIT_MENU = 'exit_menu'
EXIT_QUESTION = 'exit_question'
EXIT_TITLE = 'exit_title'
EXPORT_HTML = 'export_html'
EXPORT_XLSX = 'export_xlsx'
EXT_APK = '.apk'
EXT_EXE = '.exe'
EXT_GIF = '.gif'
EXT_JAVA = '.java'
EXT_JPEG = '.jpeg'
EXT_JPG = '.jpg'
EXT_MP4 = '.mp4'
EXT_MSI = '.msi'
EXT_PDF = '.pdf'
EXT_PNG = '.png'
EXT_ZIP = '.zip'
FALSE = False
FILE = 'file'
FIND_DUPLICATED_LINES = 'find_duplicated_lines'
FOLDER_CREATED = 'folder_info_date_added'
FOLDER_INFO_DATE_ADDED = 'folder_info_date_added'
FOLDER_INFO_DATE_MODIFIED = 'folder_info_date_modified'
FOLDER_INFO_GUID = 'folder_info_guid'
FOLDER_INFO_ID = 'folder_info_id'
FOLDER_INFO_LAST_VISITED = 'folder_info_last_visited'
FOLDER_INFO_NAME = 'folder_info_name'
FOLDER_INFO_NAME_PROPOSAL = 'folder_info_name_proposal'
FOLDER_INFO_SYNC_TRANSACTION_VERSION = 'folder_info_sync_transaction_version'
FOLDER_INFO_TYPE = 'folder_info_type'
FOLDER_INFO_URL = 'folder_info_url'
FOLDER_MODIFIED = 'folder_info_date_modified'
FOLDER_NAME = 'folder_info_name_proposal'
FONT_COURIER_NEW = 'Courier New'
FORMAT_COLUMNS = 'format_columns'
FORMAT_DATES = 'format_dates'
FORMAT_HEADER = 'format_header'
FTP_L = 'ftp'
FTP_U = 'FTP'
FULL_NAME = 'full_name'
GENERAL = 'general'
GENERATING_BOOKMARKS = 'generating_bookmarks'
GENERATING_FROM_TEXT = 'generating_from_text'
GENERATING_HTML = 'generating_html'
GENERATING_WORKBOOK = 'generating_workbook'
COMMAND_REFRESH_FOLDER_NAME = 'get_hostname'
GET_URL_STATUS = 'get_url_status'
GITHUB = 'https://github.com/vliopard/chrome2excel'
GIVEN_NAME = 'given_name'
GUID = 'guid'
GUI_PROGRESS_DIALOG = None
HIDE_COLUMNS = 'hide_columns'
HTML = 'html'
HTML_FILENAME = 'chrome.html'
HTML_FILE_FILTER = 'html_file_filter'
HTML_PARSER = 'html.parser'
HTTP = 'http'
HTTP_EQUIV = 'http-equiv'
IGNORE = 'ignore'
IMG = 'IMG'
IMPORT_ACCOUNT_DESCRIPTION = 'import_account_description'
IMPORT_ACCOUNT_MENU = 'import_account_menu'
IMPORT_TEXT_FILE = 'import_text_file'
IMPORT_TXT = 'import_txt'
INSTAGRAM = 'instagram'
INVALID_PROFILE = 'invalid_profile'
ITEM_DATE_ADDED = 'date_added'
ITEM_DATE_MODIFIED = 'date_modified'
ITEM_ICON = 'icon'
ITEM_ID = 'id'
ITEM_NAME = 'name'
ITEM_TYPE = 'type'
JAVA = 'java'
JAVASCRIPT = 'javascript'
JSCRIPT = 'JScript'
LAST_VISITED = 'last_visited'
LEFT = 'left'
LINE_LEN = screen.get_terminal_width() - 35
LINES = 'LINES'
LIST = 'list'
LIST_PROFILE = 'list_profile'
LOADING_BOOKMARKS = 'loading_bookmarks'
LOAD_TIME_OUT = 'load_time_out'
LXML = 'lxml'
MAIN = 'MAIN'
MAIN_CLEAN_HELP = 'main_clean_help'
MAIN_DESCRIPTION = 'main_description'
MAIN_FILENAME_HELP = 'main_filename_help'
MAIN_HOSTNAME_HELP = 'main_hostname_help'
MAIN_ICON = 'resources/blue.ico'
MAIN_IMPORT_HELP = 'main_import_help'
MAIN_OUTPUT_HELP = 'main_output_help'
MAIN_PROFILE_HELP = 'main_profile_help'
MAIN_REFRESH_HELP = 'main_refresh_help'
MAIN_SECTION = 'main'
MAIN_UNDUPE_HELP = 'main_undupe_help'
META = 'meta'
META_INFO = 'meta_info'
MISSING_PARAMETER = 'missing_parameter'
MP4 = 'MP4'
NEW_FOLDER = 'new_folder'
NEW_LINE = '\n'
NONAME = 'NONAME'
NONE = None
NO_ACCOUNT = 'no_account'
NO_CLEAN_URL = '[no clean url]'
NO_DATE = 'no_date'
NO_DOMAIN = '[NO_DOMAIN]'
NO_HOST_NAME = '[no hostname]'
NO_SITE_NAME = '[no site name]'
NO_TITLE = '[NO_TITLE]'
NO_PREVIOUS_TITLE = '[NO_PREVIOUS_TITLE]'
NO_URL_ADDRESS = '[no url address]'
NUMBER_FORMAT = 'YYYY/MM/DD hh:mm:ss'
OFF = 'off'
OFF_LABEL = 'off_label'
OK_BUTTON = 'ok_button'
ON = 'on'
ON_LABEL = 'on_label'
OPEN_FILE_DESCRIPTION = 'open_file_description'
OPEN_FILE_MENU = 'open_file_menu'
OPEN_GUI = 'open_gui'
OPTIONS_MENU = 'options_menu'
OUTPUT = 'output'
OUTPUT_HTML = 'output.html'
OUTPUT_NAME = 'output_name'
OUTPUT_OFF = 'output_off'
OUTPUT_ON = 'output_on'
OUTPUT_TYPE = 'output_type'
OUTPUT_XLSX = 'output.xlsx'
SYMBOL_OVERLINE = '‾'
PDF = 'PDF'
PLAYLIST = '/playlist'
PREFERENCES = 'Preferences'
PRG = 'PRG'
PROCESS_USER = 'process_user'
PROFILE = 'profile'
PROFILES = 'all'
PROFILE_CHOOSER = 'profile_chooser'
PROFILE_HELP = 'profile_help'
PROTOCOL = 'http://'
RECURSE = '\r'
COMMAND_REFRESH_URL_TITLE = 'refresh'
REFRESH_TITLE = False
REFRESH_URL_TITLE = 'refresh_url_title'
REMOVING_DUPLICATES_VALUE = 'removing_duplicates'
REPLACE = 'replace'
RESET_BUTTON = 'reset_button'
RESOLVING_HOSTNAMES = 'resolving_hostnames'
RETRIEVE_USER = 'retrieve_user'
RIGHT = 'right'
RUN_GUI = False
SAVE_FILE = 'save_file'
SAVING_HTML = 'saving_html'
SAVING_WORKBOOK = 'saving_workbook'
SET = '$set'
SETTINGS_DESCRIPTION = 'settings_description'
SETTINGS_MENU = 'settings_menu'
SETTINGS_TITLE = 'settings_title'
SIZING_COLUMNS = 'sizing_columns'
SRC = 'SRC'
STARTING_EXPORT = 'starting_export'
STATUS_BAR_FORMAT = '{desc}: {percentage:.2f}%|{bar}| {n:,}/{total:,} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
STORE_TRUE = 'store_true'
SYMBOL_AMP = '&'
SYMBOL_BLANK = ' '
SYMBOL_COLON = ':'
SYMBOL_DOT = '.'
SYMBOL_EMPTY = ''
SYMBOL_EQ = '='
SYMBOL_FORWARD_SLASHES = '//'
SYMBOL_GRADE = ' °'
SYMBOL_QM = '?'
SYMBOL_SHARP = '#'
SYMBOL_SINGLE_QUOTE = "'"
SYMBOL_SPACE = ' '
SYMBOL_UNDERLINE = '_'
SYMBOL_ZERO = '0'
SYNC_TRANSACTION_VERSION = 'sync_transaction_version'
SYSTEM_CYGWIN = 'CYGWIN'
SYSTEM_DARWIN = 'Darwin'
SYSTEM_LINUX = 'Linux'
SYSTEM_WINDOWS = 'Windows'
TAB = '\t'
TERM = 'TERM'
TEXT_CONVERT_TO_DATAFRAME = 'Convert to DataFrame...'
TEXT_CONVERT_TO_HTML = 'Convert to HTML...'
TEXT_CONVERT_TO_XLSX = 'Convert to XLSX...'
TEXT_DEBUG_MESSAGE_END = 'DEBUG MESSAGE END'
TEXT_DEBUG_MESSAGE_START = 'DEBUG MESSAGE START'
TEXT_DEFAULT = 'Default'
TEXT_DONE = 'Done.'
TEXT_FILENAME = 'chrome.txt'
TEXT_FILE_FILTER = 'text_file_filter'
TEXT_OTDS_H_CO = 'OTDS H Co.'
TEXT_REMOVING_DUPLICATES = 'Removing duplicates...'
TEXT_SORTING_DATA = 'Sorting data...'
TEXT_VERSION = '1.1'
TEXT_VINCENT_LIOPARD = 'Vincent Liopard.'
TIMEOUT = 5
TIMEOUT_LABEL = 'timeout_label'
TITLE = 'title'
TITLE_SCAPE = './/title'
TOTAL_ITEMS = 'total_items'
TRACKING_MODULE = 'tracking_module'
TRANSLATION_FILENAME = 'resources/translation.json'
TRUE = True
TXT = 'txt'
UNDUPE = 'undupe'
UNDUPE_URLS = 'undupe_urls'
UNKNOWN = 'unknown_exception'
URL_CLEAN = 'url_info_parse_address'
URL_CREATED = 'url_info_date_added'
URL_DATA_FLD = 'url_data_fld'
URL_DATA_FRAGMENT = 'url_data_fragment'
URL_DATA_HOSTNAME = 'url_data_hostname'
URL_DATA_NETLOC = 'url_data_netloc'
URL_DATA_PARAMS = 'url_data_params'
URL_DATA_PASSWORD = 'url_data_password'
URL_DATA_PATH = 'url_data_path'
URL_DATA_PORT = 'url_data_port'
URL_DATA_SCHEME = 'url_data_scheme'
URL_DATA_USERNAME = 'url_data_username'
URL_DEDUP_STATUS = 'url_dedup_status'
URL_INFO_DATE_ADDED = 'url_info_date_added'
URL_INFO_DATE_MODIFIED = 'url_info_date_modified'
URL_INFO_GUID = 'url_info_guid'
URL_INFO_ICON = 'url_info_icon'
URL_INFO_ITEM_ID = 'url_info_item_id'
URL_INFO_ITEM_TYPE = 'url_info_item_type'
URL_INFO_LAST_VISITED = 'url_info_last_visited'
URL_INFO_NAME = 'url_info_name'
URL_INFO_NAME_PREVIOUS = 'url_info_name_previous'
URL_INFO_PARSE_ADDRESS = 'url_info_parse_address'
URL_INFO_PRIME_ADDRESS = 'url_info_prime_address'
URL_INFO_SYNC_TRANSACTION_VERSION = 'url_info_sync_transaction_version'
URL_INFO_UNDUP_ADDRESS = 'url_info_undup_address'
URL_NAME = 'url_name'
URL_ORIGINAL = 'url_info_prime_address'
URL_TITLE = 'url_info_name'
USER = 'user'
USER_AGENT = 'User-Agent'
USER_HAS_NO_BOOKMARKS = 'user_has_no_bookmarks'
VIEW_SOURCE = 'view-source'
WRITE = 'w'
READ = 'r'
WARNING = 'warning'
WEBSITE_ESTADAO = 'estadao'
WEBSITE_FACEBOOK = 'facebook'
WEBSITE_FACEBOOK_COM = 'facebook.com'
WEBSITE_FOLHA = 'folha'
WEBSITE_GLOBO = 'globo'
WEBSITE_MERCADOLIVRE = 'mercadolivre'
WEBSITE_TWITTER = 'twitter'
WEBSITE_UOL = 'uol'
WEBSITE_YOUTUBE = 'youtube'
WEBSITE_YOUTUBE_COM = 'youtube.com'
WEBSITE_YOUTUBE_M = 'm.youtube.com'
WEBSITE_YOUTUBE_WWW = 'www.youtube.com'
WEBSITE_YOUTU_BE = 'youtu.be'
WORKS_ONLY_ON_CLI = 'works_only_on_cli'
WRITING_HTML = 'writing_html'
WRITING_SPREADSHEET = 'writing_spreadsheet'
XLSX = 'xlsx'
XLSX_FILENAME = 'chrome.xlsx'
XLSX_FILE_FILTER = 'xlsx_file_filter'
X_ORG_GUI = 'x_org_gui'
YOUTUBE_T = '- YouTube'
ZIP = 'ZIP'
__MAIN__ = '__main__'

display_exit_dialog = 'display_exit_dialog'
exit_dialog_confirmation = 'exit_confirmation'
export_file_type = 'export_file_type'
refresh_folder_name_with_hostname_title = 'refresh_folder_name_with_hostname_title'
refresh_url_title = 'refresh_url_title'
remove_duplicated_urls = 'remove_duplicated_urls'
remove_tracking_tokens_from_url = 'remove_tracking_tokens_from_url'
system_language = 'system_language'

SYMBOLS = ['?', '#', '&']

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

HEADERS_COMPLETE = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

label_dictionary = [
    'Folder GUID',
    'Folder ID',
    'Folder Sync',
    'Type',

    'Folder Added',
    'Folder Modified',
    'Folder visited',

    'Folder Name',
    'Folder url',

    'url GUID',
    'url ID',
    'url Sync',
    'Type',

    'url Added',
    'url Modified',
    'url Visited',

    'url Name',
    'url Clean',
    'url',
    'icon',

    'scheme',
    'netloc',
    'hostname',
    'path',
    'port',
    'param',
    'fragment',
    'username',
    'password',
]

DICTIONARY_STRUCTURE = {
    'url_dedup_status': 'url_dedup_status',
    'folder_info_guid': 'folder_info_guid',
    'folder_info_id': 'folder_info_id',
    'folder_info_sync_transaction_version': 'folder_info_sync_transaction_version',
    'folder_info_type': 'folder_info_type',
    'folder_info_date_added': 'folder_info_date_added',
    'folder_info_date_modified': 'folder_info_date_modified',
    'folder_info_last_visited': 'folder_info_last_visited',
    'folder_info_name': 'folder_info_name',
    'folder_info_url': 'folder_info_url',
    'folder_info_name_proposal': 'folder_info_name_proposal',
    'url_info_guid': 'url_info_guid',
    'url_info_item_id': 'url_info_item_id',
    'url_info_sync_transaction_version': 'url_info_sync_transaction_version',
    'url_info_item_type': 'url_info_item_type',
    'url_info_date_added': 'url_info_date_added',
    'url_info_date_modified': 'url_info_date_modified',
    'url_info_last_visited': 'url_info_last_visited',
    'url_info_parse_address': 'url_info_parse_address',
    'url_info_prime_address': 'url_info_prime_address',
    'url_info_undup_address': 'url_info_undup_address',
    'url_info_name': 'url_info_name',
    'url_info_icon': 'url_info_icon',
    'url_data_fld': 'url_data_fld',
    'url_data_scheme': 'url_data_scheme',
    'url_data_netloc': 'url_data_netloc',
    'url_data_hostname': 'url_data_hostname',
    'url_data_path': 'url_data_path',
    'url_data_port': 'url_data_port',
    'url_data_params': 'url_data_params',
    'url_data_fragment': 'url_data_fragment',
    'url_data_username': 'url_data_username',
    'url_data_password': 'url_data_password'
}


def load_translation_file():
    return load(Path(TRANSLATION_FILENAME).open(encoding=CHARSET_UTF8))


def read_tokens(category):
    cat_list = []
    with open('tokens.txt', 'r', encoding=CHARSET_UTF8) as tks:
        lines = tks.readlines()
        for line in lines:
            if line.startswith(category):
                cat_list.append(line.split('|')[1].strip())
    return cat_list


def set_language(selected_language):
    global MESSAGE
    MESSAGE = load_translation_file()[selected_language]


def get_languages():
    language_list = []
    for language_item in load_translation_file():
        language_list.append(language_item)
    return language_list


class Header:
    def __init__(self,):
        stub_date = utils.to_date(13231709218000000)

    def set_data(self, url_element):
        for key, value in url_element.items():
            setattr(self, key, value)

    def get_item(self, item_name):
        return self.__dict__[item_name]

    def to_list(self):
        dictionary = self.__dict__
        dictionary_values = []
        for dictionary_key in dictionary:
            dictionary_values.append(dictionary_key)
        return dictionary_values

    def to_dict(self):
        return self.__dict__

    def to_tuple(self):
        dictionary = self.__dict__
        dictionary_values = []
        for dictionary_key in dictionary:
            dictionary_values.append(dictionary[dictionary_key])
        return tuple(dictionary_values)

    @staticmethod
    def get_label(index):
        return label_dictionary[index]

    def to_dict_index(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)


MESSAGE = load_translation_file()[ENGLISH]

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
