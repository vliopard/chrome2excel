import os
import json
import tqdm
import shlex
import struct
import public
import platform
import subprocess

from urllib import parse
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

from openpyxl import Workbook
from openpyxl.styles import Font

from argparse import ArgumentParser
from datetime import datetime, timezone, timedelta

from htmlSupport import gettitle
from htmlExport import Folder, Urls, write_html


def get_terminal_width():
    return ((get_terminal_size()[0])-1)


def get_terminal_size():
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print("default")
        tuple_xy = (80, 25)
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_terminal_size_tput():
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


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
        return dateFromWebkit(self["date_added"])

    @property
    def modified(self):
        if "date_modified" in self:
            return dateFromWebkit(self["date_modified"])

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
        self.data = json.loads(open(path,encoding='utf-8').read())
        self.attrList = self.processRoots()
        self.urls = self.attrList["urls"]
        self.folders = self.attrList["folders"]

    def processRoots(self):
        attrList = {"urls" : [], "folders" : []}
        for key, value in json.loads(open(self.path,encoding='utf-8').read())["roots"].items():
            if "children" in value:
                self.processTree(attrList, value["children"])
        return attrList

    def processTree(self, attrList, childrenList):
        for item in childrenList:
            self.processUrls(item, attrList, childrenList)
            self.processFolders(item, attrList, childrenList)

    def processUrls(self, item, attrList, childrenList):
        if "type" in item and item["type"] == "url":
            attrList["urls"].append(Item(item))

    def processFolders(self, item, attrList, childrenList):
        if "type" in item and item["type"] == "folder":
            attrList["folders"].append(Item(item))
            if "children" in item:
                self.processTree(attrList, item["children"])


list_size = 0

words = (
    "__twitter_impression",
    "bffb",
    "client_id",
    "cmpid",
    "comment_id",
    "fb_action_ids",
    "fb_action_types",
    "fb_comment_id",
    "fbclid",
    "fbid",
    "notif_id",
    "notif_t",
    "reply_comment_id",
    "story_fbid",
    "total_comments",
    "campaign",
    "campanha",
    "gws_rd",
    "mkt_tok",
    "offset",
    "sc_campaign",
    "sc_category",
    "sc_channel",
    "sc_content",
    "sc_country",
    "sc_funnel",
    "sc_medium",
    "sc_publisher",
    "sc_segment",
    "utm_",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term"
)

youtube = (
    "sm",
    "time_continue",
    "feature",
    "app",
    "bpctr",
    "1c"
)

facebook = (
    "_rdc",
    "_rdr",
    "rc",
    "comment_tracking",
    "__tn__",
    "__xts__[0]",
    "__xts__",
    "sns",
    "hc_location",
    "pnref",
    "entry_point",
    "tab",
    "source_ref",
    "hc_ref",
    "__mref",
    "ref",
    "eid",
    "fref",
    "lst",
    "__nodl",
    "permPage",
    "notif_id"
)

data_header = [
    ('Folder GUID',     #00
     'Folder ID',       #01
     'Folder Sync',     #02
     'Type',            #03

     'Folder Added',    #04
     'Folder Modified', #05
     'Folder visited',  #06

     'Folder Name',     #07
     'Folder URL',      #08

     'URL GUID',        #09
     'URL ID',          #10
     'URL Sync',        #11
     'Type',            #12

     'URL Added',       #13
     'URL Modified',    #14
     'URL Visited',     #15

     'URL Name',        #16
     'URL Clean',       #17
     'URL',             #18
     'Scheme',          #19
     'Netloc',          #20
     'Hostname',        #21
     'Path',            #22
     'Port',            #23
     'Param',           #24
     'Fragment',        #25
     'Username',        #26
     'Password',        #27

     'ParamA',          #28
     'ParamB',          #29
     'ParamC',          #30
     'ParamD',          #31
     'ParamE',          #32
     'ParamF',          #33
     'ParamG',          #34
     'ParamH',          #35
     'ParamI',          #36
     'ParamJ',          #37
     'ParamK',          #38
     'ParamL',          #39
     'ParamM',          #40
     'ParamN',          #41
     'ParamO',          #42
     'ParamP'           #43
    )
    ]


def debug(msg):
    print(msg)


def dateFromWebkit(timestamp):
    return (datetime(1601,1,1) + timedelta(microseconds=int(timestamp))).replace(tzinfo=timezone.utc).astimezone()


def clean_url(url):
    parsed = urlparse(url)
    qd = parse_qsl(parsed.query, keep_blank_values=True)
    filtered = {}
    if parsed.hostname:
        hname = parsed.hostname
    else:
        hname = parsed.netloc
    for k, v in qd:
        if ("youtube.com" in hname or "youtu.be" in hname):
            if not k.startswith(youtube) and not k.startswith(words):
                filtered.update([(k,v)])
        elif ("facebook.com" in hname):
            if not k.startswith(facebook) and not k.startswith(words):
                filtered.update([(k,v)])
        elif not k.startswith(words):
            filtered.update([(k,v)])

    newurl = urlunparse([
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        urlencode(filtered, doseq=True),
        parsed.fragment
    ])
    return newurl


def checkNone(val):
    if val is None:
        return '[Empty]'
    return str(val)


def getUser(userpath):
    username = json.loads(open(userpath,encoding='utf-8').read())["account_info"][0]
    return username['email'], username['full_name'], username['given_name']


def parseURL(value):
    parsed = urlparse(value)
    dt = dict(parse.parse_qsl(parse.urlsplit(value).query))

    additional0 = (
                    checkNone(parsed.scheme),
                    checkNone(parsed.netloc),
                    checkNone(parsed.hostname),
                    checkNone(parsed.path),
                    checkNone(parsed.port),
                    checkNone(parsed.params),
                    checkNone(parsed.fragment),
                    checkNone(parsed.username),
                    checkNone(parsed.password)
                  )

    additional1 = ()
    for d in dt:
        additional1 = additional1 + (d+"<=>"+dt[d],)

    return additional0 + additional1


def toDate(value):
    date_value = toNumber(value)
    if date_value:
        dt = hex(int(date_value)*10)[2:17]
        microseconds = int(dt, 16) / 10
        seconds, microseconds = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 86400)
        return datetime(1601, 1, 1) + timedelta(days, seconds, microseconds)
    return None


def toNumber(value):
    if value != '[Empty]':
        return int(value)
    return None


def read_content(content):
    data = []
    for chrome_url in content:
        date_added = '[Empty]'
        date_modified = '[Empty]'
        guid = '[Empty]'
        id = '[Empty]'
        last_visited = '[Empty]'
        name = '[Empty]'
        sync_transaction_version = '[Empty]'
        type = '[Empty]'
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
                # TODO: Add icon to the spreadsheet
                icon = chrome_url[x]
            elif x == 'id':
                id = chrome_url[x]
            elif x == 'name':
                name = chrome_url[x]
            elif x == 'sync_transaction_version':
                sync_transaction_version = chrome_url[x]
            elif x == 'type':
                type = chrome_url[x]
            elif x == 'url':        
                url = chrome_url[x]
            else:
                debug('WARNING: '+str(x))
        part1 = (
                 guid,
                 toNumber(id),
                 toNumber(sync_transaction_version),
                 type,

                 toDate(date_added),
                 toDate(date_modified),
                 toDate(last_visited),

                 name,
                 clean_url(url),
                 url
                )
        part2 = parseURL(url)
        part3 = part1 + part2
        data.append (part3)
    return data


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
                debug('WARNING: '+str(x))
        f_data= (
                    f_guid,
                    toNumber(f_id),
                    toNumber(f_sync_transaction_version),
                    f_type,

                    toDate(f_date_added),
                    toDate(f_date_modified),
                    toDate(f_last_visited),

                    f_name,
                    f_url
                )

        for d in data:
            new_data = f_data + d
            data_header.append(new_data)


def get_title_conditional(pbar, disabled, url_name, url):
    url_title = ""
    if not disabled:
        pbar.update(1)
        url_title = gettitle(url)
        if url_title == -1:
            url_title = "[NO REFRESH - " + url_name + " ]"
    return url_title


def generate_html(refresh, undupe, clean):
    print("Generating html...")
    created = set()
    visited = set()
    folders = []
    data_header_undupe = []
    if undupe == 'on':
        print("_"*(get_terminal_width()))
        print("Removing duplicates...")
        print("\u203e"*(get_terminal_width()))
        with tqdm.tqdm(total=len(data_header)) as pbar:
            for a in data_header:
                pbar.update(1)
                if clean == 'on':
                    website = a[17]
                else:
                    website = a[18]
                if not website in visited:
                    visited.add(website)
                    data_header_undupe.append(a)
    else:
        data_header_undupe = data_header

    print("_"*(get_terminal_width()))
    print("Writting html...")
    print("\u203e"*(get_terminal_width()))
    with tqdm.tqdm(total=len(data_header_undupe[1:])) as pbar:
        for a in data_header_undupe[1:]:
            pbar.update(1)
            fold = a[21]
            hostname = a[21]
            if clean == 'on':
                website = a[17]
            else:
                website = a[18]

            if refresh == 'on':
                title=gettitle(website)
                if title == -1:
                    title = "[NO REFRESH - " + a[16] + " ]"

            if not fold in created:
                url = Urls(website, a[13], title)
                fold = Folder(a[4], a[5], hostname, [url])
                created.add(hostname)
                folders.append(fold)
            else:
                url = Urls(website, a[13], title)
                for x in folders:
                    if x.folder_name == hostname:
                        x.add_url(url)

    print("Saving HTML file...")
    write_html(folders)
    print("Done.")
    print("\u203e"*(get_terminal_width()))
    


def generate_workbook(refresh, undupe, clean):
    print("Generating workbook...")
    book = Workbook()
    sheet = book.active
    sheet.title = "Chrome URLs"

    visited = set()
    data_header_undupe = []
    print("Find duplicate lines...")
    if refresh != "off":
        print("_"*(get_terminal_width()))
        print("Getting URL Status...")
        print("\u203e"*(get_terminal_width()))

    disabled = True
    if refresh != "off":
        disabled = False
        
    with tqdm.tqdm(total=len(data_header),disable=disabled) as pbar:
        for a in data_header:
            if clean == 'on':
                website = a[17]
            else:
                website = a[18]
            if not website in visited:
                visited.add(website)
                data_header_undupe.append(( "MAIN", get_title_conditional(pbar, disabled, a[16], website) ) + a)
            elif undupe == "off":
                data_header_undupe.append(( "DUPE", get_title_conditional(pbar, disabled, a[16], website) ) + a)

    print("Writting spreadsheet...")
    print("\u203e"*(get_terminal_width()))
    with tqdm.tqdm(total=len(data_header_undupe)) as pbar:
        for row in data_header_undupe:
            pbar.update(1)
            sheet.append(row)

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = "A1:AT30000"

    print("_"*(get_terminal_width()))
    print("Formating columns...")
    print("\u203e"*(get_terminal_width()))
    courier = ['T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS']
    with tqdm.tqdm(total=(len(courier)*len(sheet['T']))) as pbar:
        for l in courier:
            for col_cell in sheet[l]:
                pbar.update(1)
                col_cell.font = Font(size = 10, name = 'Courier New')

    print("_"*(get_terminal_width()))
    print("Formating dates...")
    print("\u203e"*(get_terminal_width()))
    dates = ['G','H','I','P','Q','R']
    with tqdm.tqdm(total=(len(dates)*len(sheet['G']))) as pbar:
        for d in dates:
            sheet.column_dimensions[d].width = 18
            for col_cell in sheet[d]:
                pbar.update(1)
                col_cell.number_format = "YYYY/MM/DD hh:mm:ss"

    print("_"*(get_terminal_width()))
    print("Hiding columns...")
    hidden = ['C','D','E','F','G','H','I','J','K','L','Z','AA','AB','AC']
    for h in hidden:
        sheet.column_dimensions[h].width = 9
        sheet.column_dimensions[h].hidden = True

    print("Formating header...")
    for cell in sheet["1:1"]:
        cell.font = Font(bold=True)

    print("Sizing columns...")
    sheet.column_dimensions['S'].width = 30
    sheet.column_dimensions['T'].width = 85

    print("Saving workbook...")
    book.save("chrome.xlsx")
    print("Done.")
    print("\u203e"*(get_terminal_width()))


def generate_bookmarks(profile_):
    print("Generating bookmarks...")
    if profile_ == "0":
        profile_ = "Default"
    else:
        profile_ = "Profile "+profile_

    user = [
        os.path.expanduser("~/.config/google-chrome/"+profile_+"/Preferences"),
        os.path.expanduser("~/Library/Application Support/Google/Chrome/"+profile_+"/Preferences"),
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\"+profile_+"\\Preferences")
    ]

    found = False
    for f in user:
        if os.path.exists(f):
            try:
                email, full, name = getUser(f)
                found = True
            except:
                found = False
                pass
    if not found:
        print("Invalid profile.")
        exit(1)

    paths = [
        os.path.expanduser("~/.config/google-chrome/"+profile_+"/Bookmarks"),
        os.path.expanduser("~/Library/Application Support/Google/Chrome/"+profile_+"/Bookmarks"),
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\"+profile_+"\\Bookmarks")
    ]

    for f in paths:
        if os.path.exists(f):
            return email, full, name, Bookmarks(f)


def run_chrome(profile, refresh, undupe, output, clean):
    print("\n\n")
    print("_"*(get_terminal_width()))
    print("Starting Chrome Bookmars export.")
    email, full, name, bookmarks = generate_bookmarks(profile)
    print("_"*(get_terminal_width()))
    print("Processing user: {",full,"} ["+email+"]")
    print("\u203e"*(get_terminal_width()))
    generate_data(bookmarks)
    if output == "xlsx":
        generate_workbook(refresh, undupe, clean)
    else:
        generate_html(refresh, undupe, clean)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script to extract bookmarks from Google Chrome to Microsoft Excel Spreadsheet."
    )
    parser.add_argument(
        "--profile",
        "-p",
        help="Profile number to extract: 0 Default.",
        default = "0"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file type [html, xlsx]: xlsx Default.",
        default = "xlsx"
    )
    parser.add_argument(
        "--refresh",
        "-r",
        help="Refresh URL Title [on, off]: off Default.",
        default = "off"
    )
    parser.add_argument(
        "--undupe",
        "-u",
        help="Remove duplicated URL [on, off]: off Default.",
        default = "off"
    )
    parser.add_argument(
        "--clean",
        "-c",
        help="Remove trackers from URL [on, off]: off Default.",
        default = "off"
    )

    args = vars(parser.parse_args())
    run_chrome(**args)
