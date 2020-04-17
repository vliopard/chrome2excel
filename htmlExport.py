import tools


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
    ret = new_line()+new_tab()+'<DT><H3 ADD_DATE="'+tools.dateToWebkit(add_date)+'" LAST_MODIFIED="'+tools.dateToWebkit(modified_date)+'">'+folder_name+'</H3>'+new_line()+new_tab()+'<DL><p>'
    level = level + 1
    return ret


def close_folder():
    global level
    level = level - 1
    ret = new_line()+new_tab()+'</DL><p>'
    return ret


def add_url(url, add_date, url_title):
    return new_line()+new_tab()+'<DT><A HREF="'+str(url).strip()+'" ADD_DATE="'+tools.dateToWebkit(add_date)+'">'+str(url_title)+'</A>'


def new_line():
    return "\n"


def new_tab():
    global level
    return "\t"*level


def write_html(fold):
    with open('chrome.html', 'w', encoding='utf-8') as chrome_html:
        chrome_html.write(header)

        for item in fold:
            if isinstance(item, tools.Folder):
                chrome_html.write(open_folder(item.add_date, item.modify_date, item.folder_name))
                for url in item.children:
                    if isinstance(url, tools.Urls):
                        chrome_html.write(add_url(url.url, url.add_date, url.title))
                    elif isinstance (url, tools.Folder):
                        print("New Folder")
                chrome_html.write(close_folder())

        chrome_html.write(tail)
