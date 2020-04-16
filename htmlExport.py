from datetime import datetime

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


def dateToWebkit(date_string):
    if date_string:
        diff = date_string - datetime(1601, 1, 1)
        seconds_in_day = 60 * 60 * 24
        value = '{:<010d}'.format(diff.days * seconds_in_day + diff.seconds + diff.microseconds)
        return str(value)
    return("")


header = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>"""
tail = """\n</DL><p>"""

level = 1

def open_folder(add_date, modified_date, folder_name):
    global level
    ret = new_line()+new_tab()+'<DT><H3 ADD_DATE="'+dateToWebkit(add_date)+'" LAST_MODIFIED="'+dateToWebkit(modified_date)+'">'+folder_name+'</H3>'+new_line()+new_tab()+'<DL><p>'
    level = level + 1
    return ret


def close_folder():
    global level
    level = level - 1
    ret = new_line()+new_tab()+'</DL><p>'
    return ret


def add_url(url, add_date, url_title):
    return new_line()+new_tab()+'<DT><A HREF="'+str(url)+'" ADD_DATE="'+dateToWebkit(add_date)+'">'+str(url_title)+'</A>'


def new_line():
    return "\n"


def new_tab():
    global level
    return "\t"*level


def write_html(fold):
    with open('chrome.html', 'w') as chrome_html:
        chrome_html.write(header)

        for item in fold:
            if isinstance(item, Folder):
                chrome_html.write(open_folder(item.add_date, item.modify_date, item.folder_name))
                for url in item.children:
                    if isinstance(url, Urls):
                        chrome_html.write(add_url(url.url, url.add_date, url.title))
                    elif isinstance (url, Folder):
                        print("New Folder")
                chrome_html.write(close_folder())

        chrome_html.write(tail)
