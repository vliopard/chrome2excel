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


def get_title_conditional(pbar, disabled, url_name, url):
    url_title = None
    if not disabled:
        pbar.update(1)
        nro, url_title = htmlSupport.gettitle(url)
        if nro != 0:
            url_title = "[ " + url_title + " " + str(nro) + " - " + url_name + " ]"
    return url_title


def import_text(txt="chrome.txt"):
    tools.display("Importing text file...")
    url_list = []
    with open(txt, encoding='utf-8') as bm:
        for line in bm:
            url_list.append(line)
    return url_list


def append_dataheader(data_header, url_list):
    tools.display("Appending dataheader...")
    for line in url_list:
        url_parts = htmlSupport.parseURL(line)
        # stub_date = tools.toDate(13231709218000000)
        head = preset.Header()
        head.Hostname = url_parts[2]
        #######################################################################################
        # TODO: If not enabled, returns current name or url
        #######################################################################################
        head.URL_Clean = htmlSupport.clean_url(line)
        head.URL = line
        element = head.toTuple()
        '''
        element = ('Folder GUID', 'Folder ID', 'Folder Sync', 'Type',
                   stub_date, stub_date, stub_date, 'Folder Name',
                   'Folder URL', 'URL GUID', 'URL ID', 'URL Sync', 'Type',
                   stub_date, stub_date, stub_date, 'URL Name',
                   htmlSupport.clean_url(line), line, 'Scheme', 'Netloc', url_parts[2],
                   'Path', 'Port', 'Param', 'Fragment', 'Username', 'Password',
                   'ParamA', 'ParamB', 'ParamC', 'ParamD', 'ParamE', 'ParamF',
                   'ParamG', 'ParamH', 'ParamI', 'ParamJ', 'ParamK', 'ParamL',
                   'ParamM', 'ParamN', 'ParamO', 'ParamP')
        '''
        data_header.append(element)
    return data_header


def generate_from_txt(url_list):
    tools.display("Generating from TXT...")
    txt_header = []
    return append_dataheader(txt_header, url_list)


def generate_html(data_header, refresh, undupe, clean, import_txt, checkhost):
    #######################################################################################
    # TODO: SETTINGS MUST BE AVAILABLE BY SETTINGS LOAD FUNCTION
    #######################################################################################
    tools.display("Generating html...")

    data_header = append_dataheader(data_header, import_text())

    created = set()
    visited = set()
    folders = []
    data_header_undupe = []
    if undupe == 'on':
        tools.display("_"*(screenSupport.get_terminal_width()))
        tools.display("Removing duplicates...")
        tools.display("\u203e"*(screenSupport.get_terminal_width()))
        with tqdm.tqdm(total=len(data_header)) as pbar:
            for a in data_header:
                pbar.update(1)
                if clean == 'on':
                    website = a[17]
                else:
                    website = a[18]
                if website not in visited:
                    visited.add(website)
                    data_header_undupe.append(a)
    else:
        data_header_undupe = data_header

    tools.display("_"*(screenSupport.get_terminal_width()))
    tools.display("Writting html...")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))
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

            if checkhost == 'on':
                nro, hostname = htmlSupport.gettitle("http://"+host_name)
                if nro != 0:
                    hostname = "[ " + hostname + " " + str(nro) + " - " + host_name + " ]"

            if hostname not in created:
                url = tools.Urls(website, a[13], title)
                fold = tools.Folder(a[4], a[5], hostname, [url])
                created.add(hostname)
                folders.append(fold)
            else:
                url = tools.Urls(website, a[13], title)
                for x in folders:
                    if x.folder_name == hostname:
                        x.add_url(url)

    tools.display("_"*(screenSupport.get_terminal_width()))
    tools.display("Saving HTML file...")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))
    htmlExport.write_html(folders)
    tools.display("Done.")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))


def generate_workbook(data_header, refresh, undupe, clean):
    tools.display("Generating workbook...")
    book = Workbook()
    sheet = book.active
    sheet.title = "Chrome URLs"

    visited = set()
    data_header_undupe = []
    tools.display("Find duplicate lines...")
    if refresh != "off":
        tools.display("_"*(screenSupport.get_terminal_width()))
        tools.display("Getting URL Status...")
        tools.display("\u203e"*(screenSupport.get_terminal_width()))

    disabled = True
    if refresh != "off":
        disabled = False

    with tqdm.tqdm(total=len(data_header), disable=disabled) as pbar:
        for a in data_header:
            if clean == 'on':
                website = a[17]
            else:
                website = a[18]
            if website not in visited:
                visited.add(website)
                data_header_undupe.append(("MAIN", get_title_conditional(pbar, disabled, a[16], website)) + a)
            elif undupe == "off":
                data_header_undupe.append(("DUPE", get_title_conditional(pbar, disabled, a[16], website)) + a)

    tools.display("Writting spreadsheet...")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))
    with tqdm.tqdm(total=len(data_header_undupe)) as pbar:
        for row in data_header_undupe:
            pbar.update(1)
            sheet.append(row)

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = "A1:AT30000"

    tools.display("_"*(screenSupport.get_terminal_width()))
    tools.display("Formating columns...")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))
    courier = ['T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               'AA', 'AB', 'AC', 'AD', 'AE', 'AF',
               'AG', 'AH', 'AI', 'AJ', 'AK', 'AL',
               'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS']
    with tqdm.tqdm(total=(len(courier)*len(sheet['T']))) as pbar:
        for l in courier:
            for col_cell in sheet[l]:
                pbar.update(1)
                col_cell.font = Font(size=10, name='Courier New')

    tools.display("_"*(screenSupport.get_terminal_width()))
    tools.display("Formating dates...")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))
    dates = ['G', 'H', 'I', 'P', 'Q', 'R']
    with tqdm.tqdm(total=(len(dates)*len(sheet['G']))) as pbar:
        for d in dates:
            sheet.column_dimensions[d].width = 18
            for col_cell in sheet[d]:
                pbar.update(1)
                col_cell.number_format = "YYYY/MM/DD hh:mm:ss"

    tools.display("_"*(screenSupport.get_terminal_width()))
    tools.display("Hiding columns...")
    hidden = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Z', 'AA', 'AB', 'AC']
    for h in hidden:
        sheet.column_dimensions[h].width = 9
        sheet.column_dimensions[h].hidden = True

    tools.display("Formating header...")
    for cell in sheet["1:1"]:
        cell.font = Font(bold=True)

    tools.display("Sizing columns...")
    sheet.column_dimensions['S'].width = 30
    sheet.column_dimensions['T'].width = 85

    tools.display("Saving workbook...")
    book.save("chrome.xlsx")
    tools.display("Done.")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))


def get_User(profile_):
    tools.display("Retrieving user...")
    found = False
    for f in preset.retUser(profile_):
        if os.path.exists(f):
            try:
                email, full, name = chromeProfile.getUser(f)
                found = True
            except Exception:
                found = False
                pass
    if not found:
        tools.display("Invalid profile.")
        exit(1)
    return email, full, name


def run_chrome(profile, refresh, undupe, output, clean, import_txt, get_hostname):
    tools.display("\n\n")
    tools.display("_"*(screenSupport.get_terminal_width()))
    tools.display("Starting Chrome Bookmars export.")
    email, full, name = get_User(profile)
    bookmarks = bookMarks.generate_bookmarks(profile)
    tools.display("_"*(screenSupport.get_terminal_width()))
    tools.display("Processing user: {", full, "} [" + email + "]")
    tools.display("\u203e"*(screenSupport.get_terminal_width()))
    bookmarks_data = bookMarks.generate_data(bookmarks)
    if output == "xlsx":
        generate_workbook(bookmarks_data, refresh, undupe, clean)
    else:
        generate_html(bookmarks_data, refresh, undupe, clean, import_txt, get_hostname)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script to extract bookmarks from Google Chrome to Microsoft Excel Spreadsheet."
    )
    parser.add_argument(
        "--profile",
        "-p",
        help="Profile number to extract: 0 Default.",
        default="0"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file type [html, xlsx]: xlsx Default.",
        default="xlsx"
    )
    parser.add_argument(
        "--refresh",
        "-r",
        help="Refresh URL Title [on, off]: off Default.",
        default="off"
    )
    parser.add_argument(
        "--undupe",
        "-u",
        help="Remove duplicated URL [on, off]: off Default.",
        default="off"
    )
    parser.add_argument(
        "--clean",
        "-c",
        help="Remove trackers from URL [on, off]: off Default.",
        default="off"
    )
    parser.add_argument(
        "--import_txt",
        "-i",
        help="Import TXT file [on, off]: off Default.",
        default="off"
    )
    parser.add_argument(
        "--get_hostname",
        "-g",
        help="Get hostname [on, off]: off Default.",
        default="off"
    )

    args = vars(parser.parse_args())
    run_chrome(**args)
