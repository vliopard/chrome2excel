import os
import tqdm
import tools
import preset
import bookMarks

import htmlExport
import htmlSupport
import screenSupport
import chromeProfile

from openpyxl import Workbook
from openpyxl.styles import Font

from argparse import ArgumentParser


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
                # TODO: Add icon to the spreadsheet
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
                 tools.toNumber(item_id),
                 tools.toNumber(sync_transaction_version),
                 item_type,

                 tools.toDate(date_added),
                 tools.toDate(date_modified),
                 tools.toDate(last_visited),

                 name,
                 htmlSupport.clean_url(url),
                 url
                )
        part2 = htmlSupport.parseURL(url)
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
                tools.debug('WARNING: '+str(x))
        f_data= (
                    f_guid,
                    tools.toNumber(f_id),
                    tools.toNumber(f_sync_transaction_version),
                    f_type,

                    tools.toDate(f_date_added),
                    tools.toDate(f_date_modified),
                    tools.toDate(f_last_visited),

                    f_name,
                    f_url
                )

        for d in data:
            new_data = f_data + d
            preset.data_header.append(new_data)


def get_title_conditional(pbar, disabled, url_name, url):
    url_title = None
    if not disabled:
        pbar.update(1)
        nro, url_title = htmlSupport.gettitle(url)
        if nro != 0:
            url_title = "[ " + url_title + " " + str(nro) + " - " + url_name + " ]"
    return url_title


def import_txt():
    print("Importing text file...")
    url_list = []
    with open("chrome.txt",encoding='utf-8') as bm:
        for line in bm:
            url_list.append(line)
    return url_list


def append_dataheader(url_list):
    print("Appending dataheader...")
    for line in url_list:
        url_parts = htmlSupport.parseURL(line)
        stub_date =  tools.toDate(131636882970000)
        element = ('Folder GUID', 'Folder ID', 'Folder Sync', 'Type', 
                   stub_date, stub_date, stub_date, 'Folder Name', 
                   'Folder URL', 'URL GUID', 'URL ID', 'URL Sync', 'Type',
                   stub_date, stub_date, stub_date, 'URL Name', 
                   htmlSupport.clean_url(line), line, 'Scheme', 'Netloc', url_parts[2], 
                   'Path', 'Port', 'Param', 'Fragment', 'Username', 'Password', 
                   'ParamA', 'ParamB', 'ParamC', 'ParamD', 'ParamE', 'ParamF', 
                   'ParamG', 'ParamH', 'ParamI', 'ParamJ', 'ParamK', 'ParamL', 
                   'ParamM', 'ParamN', 'ParamO', 'ParamP' )
        preset.data_header.append(element)


def generate_html(refresh, undupe, clean, input):
    print("Generating html...")
    
    append_dataheader(import_txt())
    
    created = set()
    visited = set()
    folders = []
    data_header_undupe = []
    if undupe == 'on':
        print("_"*(screenSupport.get_terminal_width()))
        print("Removing duplicates...")
        print("\u203e"*(screenSupport.get_terminal_width()))
        with tqdm.tqdm(total=len(preset.data_header)) as pbar:
            for a in preset.data_header:
                pbar.update(1)
                if clean == 'on':
                    website = a[17]
                else:
                    website = a[18]
                if not website in visited:
                    visited.add(website)
                    data_header_undupe.append(a)
    else:
        data_header_undupe = preset.data_header

    print("_"*(screenSupport.get_terminal_width()))
    print("Writting html...")
    print("\u203e"*(screenSupport.get_terminal_width()))
    with tqdm.tqdm(total=len(data_header_undupe[1:])) as pbar:
        for a in data_header_undupe[1:]:
            pbar.update(1)

            title = a[16]

            if clean == 'on':
                website = a[17]
            else:
                website = a[18]

            hostname = a[21]
            host_name = a[21]

            if refresh == 'on':

                nro, title = htmlSupport.gettitle(website)
                if nro != 0:
                    title = "[ " + title + " " + str(nro) + " - " + a[16] + " ]"

                nro, hostname = htmlSupport.gettitle("http://"+host_name)
                if nro != 0:
                    hostname = "[ " + hostname + " " + str(nro) + " - " + host_name + " ]"

            if not hostname in created:
                url = tools.Urls(website, a[13], title)
                fold = tools.Folder(a[4], a[5], hostname, [url])
                created.add(hostname)
                folders.append(fold)
            else:
                url = tools.Urls(website, a[13], title)
                for x in folders:
                    if x.folder_name == hostname:
                        x.add_url(url)

    print("_"*(screenSupport.get_terminal_width()))
    print("Saving HTML file...")
    print("\u203e"*(screenSupport.get_terminal_width()))
    htmlExport.write_html(folders)
    print("Done.")
    print("\u203e"*(screenSupport.get_terminal_width()))


def generate_workbook(refresh, undupe, clean):
    print("Generating workbook...")
    book = Workbook()
    sheet = book.active
    sheet.title = "Chrome URLs"

    visited = set()
    data_header_undupe = []
    print("Find duplicate lines...")
    if refresh != "off":
        print("_"*(screenSupport.get_terminal_width()))
        print("Getting URL Status...")
        print("\u203e"*(screenSupport.get_terminal_width()))

    disabled = True
    if refresh != "off":
        disabled = False
        
    with tqdm.tqdm(total=len(preset.data_header),disable=disabled) as pbar:
        for a in preset.data_header:
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
    print("\u203e"*(screenSupport.get_terminal_width()))
    with tqdm.tqdm(total=len(data_header_undupe)) as pbar:
        for row in data_header_undupe:
            pbar.update(1)
            sheet.append(row)

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = "A1:AT30000"

    print("_"*(screenSupport.get_terminal_width()))
    print("Formating columns...")
    print("\u203e"*(screenSupport.get_terminal_width()))
    courier = ['T','U','V','W','X','Y','Z',
               'AA','AB','AC','AD','AE','AF',
               'AG','AH','AI','AJ','AK','AL',
               'AM','AN','AO','AP','AQ','AR','AS']
    with tqdm.tqdm(total=(len(courier)*len(sheet['T']))) as pbar:
        for l in courier:
            for col_cell in sheet[l]:
                pbar.update(1)
                col_cell.font = Font(size = 10, name = 'Courier New')

    print("_"*(screenSupport.get_terminal_width()))
    print("Formating dates...")
    print("\u203e"*(screenSupport.get_terminal_width()))
    dates = ['G','H','I','P','Q','R']
    with tqdm.tqdm(total=(len(dates)*len(sheet['G']))) as pbar:
        for d in dates:
            sheet.column_dimensions[d].width = 18
            for col_cell in sheet[d]:
                pbar.update(1)
                col_cell.number_format = "YYYY/MM/DD hh:mm:ss"

    print("_"*(screenSupport.get_terminal_width()))
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
    print("\u203e"*(screenSupport.get_terminal_width()))


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
                email, full, name = chromeProfile.getUser(f)
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
            return email, full, name, bookMarks.Bookmarks(f)


def run_chrome(profile, refresh, undupe, output, clean, input):
    print("\n\n")
    print("_"*(screenSupport.get_terminal_width()))
    print("Starting Chrome Bookmars export.")
    email, full, name, bookmarks = generate_bookmarks(profile)
    print("_"*(screenSupport.get_terminal_width()))
    print("Processing user: {",full,"} ["+email+"]")
    print("\u203e"*(screenSupport.get_terminal_width()))
    generate_data(bookmarks)
    if output == "xlsx":
        generate_workbook(refresh, undupe, clean)
    else:
        generate_html(refresh, undupe, clean, input)


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
    parser.add_argument(
        "--input",
        "-i",
        help="Import TXT file [on, off]: off Default.",
        default = "off"
    )

    args = vars(parser.parse_args())
    run_chrome(**args)
