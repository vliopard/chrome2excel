import tqdm
import tools
import utils
import preset
import bookMarks

import htmlExport
import htmlSupport
import screenSupport
import chromeProfile

from openpyxl import Workbook
from openpyxl.styles import Font

from argparse import ArgumentParser


def get_title_conditional(progress_bar, get_title_disabled, url_name, url_address):
    if not get_title_disabled:
        progress_bar.update(1)
        status_number, url_title = htmlSupport.get_title(url_address)
        if status_number != 0:
            url_title = "[ " + url_title + " " + str(status_number) + " - " + url_name + " ]"
        return url_title
    return url_name


def import_text_file(text_file=preset.text_filename):
    tools.display(preset.message["import_text_file"])
    url_list = []
    with open(text_file, encoding='utf-8') as text_file:
        for url_item in text_file:
            url_list.append(url_item.strip())
    return url_list


def append_data_table(data_table, url_list):
    tools.display(preset.message["appending_data_table"])
    for url_item in url_list:
        head = preset.Header()
        head.Hostname = htmlSupport.parse_url(url_item)[2]
        #######################################################################################
        # TODO: If not enabled, returns current name or url
        #######################################################################################
        head.URL_Clean = htmlSupport.clean_url(url_item)
        head.URL = url_item
        data_table.append(head.to_tuple())
    return data_table


def generate_from_txt(url_list):
    tools.display(preset.message["generating_from_text"])
    txt_header = []
    return append_data_table(txt_header, url_list)


def generate_html(data_table, reload_url_title, remove_duplicated_urls, remove_tracking_from_url, import_txt, get_hostname_title):
    #######################################################################################
    # TODO: SETTINGS MUST BE AVAILABLE BY SETTINGS LOAD FUNCTION
    #######################################################################################
    tools.display(preset.message["generating_html"])

    data_table = append_data_table(data_table, import_text_file())
    visited_hostname_title = set()
    visited_url_address = set()
    folder_list = []
    data_table_without_duplicates = []
    if remove_duplicated_urls == preset.on:
        tools.display(preset.underline*(screenSupport.get_terminal_width()))
        tools.display(preset.message["removing_duplicates"])
        tools.display(preset.overline*(screenSupport.get_terminal_width()))
        with tqdm.tqdm(total=len(data_table)) as progress_bar:
            for data_row in data_table:
                progress_bar.update(1)
                if remove_tracking_from_url == preset.on:
                    url_address = data_row[17]
                else:
                    url_address = data_row[18]
                if url_address not in visited_url_address:
                    visited_url_address.add(url_address)
                    data_table_without_duplicates.append(data_row)
    else:
        data_table_without_duplicates = data_table

    tools.display(preset.underline*(screenSupport.get_terminal_width()))
    tools.display(preset.message["writing_html"])
    tools.display(preset.overline*(screenSupport.get_terminal_width()))
    with tqdm.tqdm(total=len(data_table_without_duplicates[1:])) as progress_bar:
        for data_row in data_table_without_duplicates[1:]:
            progress_bar.update(1)

            url_title = data_row[16]

            if remove_tracking_from_url == preset.on:
                url_address = data_row[17]
            else:
                url_address = data_row[18]

            hostname_title = data_row[21]
            original_hostname = data_row[21]

            if reload_url_title == preset.on:
                status_number, url_title = htmlSupport.get_title(url_address)
                if status_number != 0:
                    url_title = "[ " + url_title + " " + str(status_number) + " - " + data_row[16] + " ]"

            if get_hostname_title == preset.on:
                status_number, hostname_title = htmlSupport.get_title(preset.protocol + original_hostname)
                if status_number != 0:
                    hostname_title = "[ " + hostname_title + " " + str(status_number) + " - " + original_hostname + " ]"

            if hostname_title not in visited_hostname_title:
                url_data = tools.Urls(url_address, data_row[13], url_title)
                visited_hostname_title.add(hostname_title)
                folder_list.append(tools.Folder(data_row[4], data_row[5], hostname_title, [url_data]))
            else:
                url_data = tools.Urls(url_address, data_row[13], url_title)
                for folder in folder_list:
                    if folder.folder_name == hostname_title:
                        folder.add_url(url_data)

    tools.display(preset.underline*(screenSupport.get_terminal_width()))
    tools.display(preset.message["saving_html"])
    tools.display(preset.overline*(screenSupport.get_terminal_width()))
    htmlExport.write_html(folder_list)
    tools.display(preset.message["done"])
    tools.display(preset.overline*(screenSupport.get_terminal_width()))


def generate_workbook(data_table, reload_url_title, remove_duplicated_urls, remove_tracking_from_url):
    tools.display(preset.message["generating_workbook"])
    excel_workbook = Workbook()
    excel_worksheet = excel_workbook.active
    excel_worksheet.title = preset.message["chrome_urls"]

    visited_url_address = set()
    data_table_without_duplicates = []
    tools.display(preset.message["find_duplicated_lines"])
    if reload_url_title != preset.off:
        tools.display(preset.underline*(screenSupport.get_terminal_width()))
        tools.display(preset.message["get_url_status"])
        tools.display(preset.overline*(screenSupport.get_terminal_width()))

    reload_url_title_disabled = True
    if reload_url_title != preset.off:
        reload_url_title_disabled = False

    with tqdm.tqdm(total=len(data_table), disable=reload_url_title_disabled) as progress_bar:
        for data_row in data_table:
            if remove_tracking_from_url == preset.on:
                url_address = data_row[17]
            else:
                url_address = data_row[18]
            if url_address not in visited_url_address:
                visited_url_address.add(url_address)
                data_table_without_duplicates.append(("MAIN", get_title_conditional(progress_bar, reload_url_title_disabled, data_row[16], url_address)) + data_row)
            elif remove_duplicated_urls == preset.off:
                data_table_without_duplicates.append(("DUPE", get_title_conditional(progress_bar, reload_url_title_disabled, data_row[16], url_address)) + data_row)

    tools.display(preset.message["writing_spreadsheet"])
    tools.display(preset.overline*(screenSupport.get_terminal_width()))
    with tqdm.tqdm(total=len(data_table_without_duplicates)) as progress_bar:
        for data_row in data_table_without_duplicates:
            progress_bar.update(1)
            excel_worksheet.append(data_row)

    excel_worksheet.freeze_panes = "A2"
    excel_worksheet.auto_filter.ref = "A1:AT30000"

    tools.display(preset.underline*(screenSupport.get_terminal_width()))
    tools.display(preset.message["format_columns"])
    tools.display(preset.overline*(screenSupport.get_terminal_width()))
    font_columns = ['T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               'AA', 'AB', 'AC', 'AD', 'AE', 'AF',
               'AG', 'AH', 'AI', 'AJ', 'AK', 'AL',
               'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS']
    with tqdm.tqdm(total=(len(font_columns)*len(excel_worksheet['T']))) as progress_bar:
        for font_column in font_columns:
            for worksheet_column in excel_worksheet[font_column]:
                progress_bar.update(1)
                worksheet_column.font = Font(size=10, name='Courier New')

    tools.display(preset.underline*(screenSupport.get_terminal_width()))
    tools.display(preset.message["format_dates"])
    tools.display(preset.overline*(screenSupport.get_terminal_width()))
    date_columns = ['G', 'H', 'I', 'P', 'Q', 'R']
    with tqdm.tqdm(total=(len(date_columns)*len(excel_worksheet['G']))) as progress_bar:
        for date_column in date_columns:
            excel_worksheet.column_dimensions[date_column].width = 18
            for worksheet_column in excel_worksheet[date_column]:
                progress_bar.update(1)
                worksheet_column.number_format = preset.number_format

    tools.display(preset.underline*(screenSupport.get_terminal_width()))
    tools.display(preset.message["hide_columns"])
    hidden_columns = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Z', 'AA', 'AB', 'AC']
    for h in hidden_columns:
        excel_worksheet.column_dimensions[h].width = 9
        excel_worksheet.column_dimensions[h].hidden = True

    tools.display(preset.message["format_header"])
    for cell in excel_worksheet["1:1"]:
        cell.font = Font(bold=True)

    tools.display(preset.message["sizing_columns"])
    excel_worksheet.column_dimensions['S'].width = 30
    excel_worksheet.column_dimensions['T'].width = 85

    tools.display(preset.message["saving_bookmarks"])
    excel_workbook.save(preset.xlsx_filename)
    tools.display(preset.message["done"])
    tools.display(preset.overline*(screenSupport.get_terminal_width()))


def get_profile(profile):
    tools.display(preset.message["retrieve_user"])
    user_data = tools.get_chrome_element(profile, preset.preferences)
    tools.debug("GET_PROFILE: user_data[" + user_data + "]")
    if not user_data:
        tools.display(preset.message["invalid_profile"])
        exit(1)
    return chromeProfile.get_user(user_data)


def run_chrome(profile, refresh, undupe, output, clean, import_txt, get_hostname):
    tools.debug("RUN_CHROME: profile[", profile,
                "] refresh[", refresh,
                "] undupe[", undupe,
                "] output[", output,
                "] clean[", clean,
                "] import[", import_txt,
                "] hostname[", get_hostname)
    tools.display(preset.new_line+preset.new_line)
    tools.display(preset.underline*(screenSupport.get_terminal_width()))
    tools.display(preset.message["starting_export"])
    email, full, name = get_profile(profile)
    tools.debug("GET_PROFILE: email[", email,
                "] full[", full,
                "] name[", name)
    bookmarks = bookMarks.generate_bookmarks(profile)
    tools.display(preset.underline*(screenSupport.get_terminal_width()))
    tools.display(preset.message["process_user"] + ": {", full, "} [" + email + "]")
    tools.display(preset.overline*(screenSupport.get_terminal_width()))
    bookmarks_data = bookMarks.generate_data(bookmarks)
    if output == "xlsx":
        generate_workbook(bookmarks_data, refresh, undupe, clean)
    else:
        generate_html(bookmarks_data, refresh, undupe, clean, import_txt, get_hostname)


if __name__ == "__main__":
    argument_parser = ArgumentParser(
        description=preset.message["main_description"]
    )
    argument_parser.add_argument(
        "--profile",
        "-p",
        help=preset.message["main_profile_help"],
        default="0"
    )
    argument_parser.add_argument(
        "--output",
        "-o",
        help=preset.message["main_output_help"],
        default="xlsx"
    )
    argument_parser.add_argument(
        "--refresh",
        "-r",
        help=preset.message["main_refresh_help"],
        default=preset.off
    )
    argument_parser.add_argument(
        "--undupe",
        "-u",
        help=preset.message["main_undupe_help"],
        default=preset.off
    )
    argument_parser.add_argument(
        "--clean",
        "-c",
        help=preset.message["main_clean_help"],
        default=preset.off
    )
    argument_parser.add_argument(
        "--import_txt",
        "-i",
        help=preset.message["main_import_help"],
        default=preset.off
    )
    argument_parser.add_argument(
        "--get_hostname",
        "-g",
        help=preset.message["main_hostname_help"],
        default=preset.off
    )

    arguments = vars(argument_parser.parse_args())
    run_chrome(**arguments)
