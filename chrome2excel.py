import tqdm
import tools
import preset
import bookMarks

import htmlExport
import htmlSupport
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
    tools.underline()
    tools.display(preset.message["import_text_file"] + " [" + text_file + "]")
    tools.overline()
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
        head.URL_Clean = htmlSupport.clean_url(url_item)
        head.URL = url_item
        data_table.append(head.to_tuple())
    return data_table


def generate_from_txt(url_list):
    tools.display(preset.message["generating_from_text"])
    txt_header = []
    return append_data_table(txt_header, url_list)


def generate_web_page(web_page_filename, data_table, reload_url_title, remove_duplicated_urls, remove_tracking_from_url, get_hostname_title):
    tools.display(preset.message["generating_html"] + " [" + web_page_filename + "]")

    visited_hostname_title = set()
    visited_url_address = set()
    folder_list = []
    data_table_without_duplicates = []
    if remove_duplicated_urls == preset.on:
        tools.underline()
        tools.display(preset.message["removing_duplicates"])
        tools.overline()
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

    tools.underline()
    tools.display(preset.message["writing_html"])
    tools.overline()
    with tqdm.tqdm(total=len(data_table_without_duplicates)) as progress_bar:
        for data_row in data_table_without_duplicates:
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

    tools.underline()
    tools.display(preset.message["saving_html"])
    tools.overline()
    htmlExport.write_html(web_page_filename, folder_list)
    tools.display(preset.message["done"])
    tools.overline()


def generate_work_book(spreadsheet_filename, data_table, reload_url_title, remove_duplicated_urls, remove_tracking_from_url, get_hostname_title):
    tools.display(preset.message["generating_workbook"] + " [" + spreadsheet_filename + "]")
    excel_workbook = Workbook()
    excel_worksheet = excel_workbook.active
    excel_worksheet.title = preset.message["chrome_urls"]

    visited_url_address = set()
    data_table_without_duplicates = []
    tools.display(preset.message["find_duplicated_lines"])
    reload_url_title_disabled = True
    if reload_url_title != preset.off:
        tools.underline()
        tools.display(preset.message["get_url_status"])
        tools.overline()
        reload_url_title_disabled = False

    with tqdm.tqdm(total=len(data_table), disable=reload_url_title_disabled) as progress_bar:
        for data_row in data_table:
            #######################################################################################
            # TODO: IF get_hostname_title: UPDATE FOLDERNAME WITH HOST GET TITLE
            #######################################################################################
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
    tools.overline()
    with tqdm.tqdm(total=len(data_table_without_duplicates)) as progress_bar:
        data_row_header = ["DUPE", "HOSTNAME"]
        for item in preset.label_dictionary:
            data_row_header.append(preset.label_dictionary[item])
        excel_worksheet.append(tuple(data_row_header))
        progress_bar.update(1)
        for data_row in data_table_without_duplicates:
            progress_bar.update(1)
            excel_worksheet.append(data_row)

    excel_worksheet.freeze_panes = "A2"
    excel_worksheet.auto_filter.ref = "A1:AT30000"

    tools.underline()
    tools.display(preset.message["format_columns"])
    tools.overline()
    font_columns = ['T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    'AA', 'AB', 'AC', 'AD', 'AE', 'AF',
                    'AG', 'AH', 'AI', 'AJ', 'AK', 'AL',
                    'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS']
    with tqdm.tqdm(total=(len(font_columns)*len(excel_worksheet['T']))) as progress_bar:
        for font_column in font_columns:
            for worksheet_column in excel_worksheet[font_column]:
                progress_bar.update(1)
                worksheet_column.font = Font(size=10, name='Courier New')

    tools.underline()
    tools.display(preset.message["format_dates"])
    tools.overline()
    date_columns = ['G', 'H', 'I', 'P', 'Q', 'R']
    with tqdm.tqdm(total=(len(date_columns)*len(excel_worksheet['G']))) as progress_bar:
        for date_column in date_columns:
            excel_worksheet.column_dimensions[date_column].width = 18
            for worksheet_column in excel_worksheet[date_column]:
                progress_bar.update(1)
                worksheet_column.number_format = preset.number_format

    tools.underline()
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

    tools.display(preset.message["saving_workbook"])
    excel_workbook.save(spreadsheet_filename)
    tools.display(preset.message["done"])
    tools.overline()


def get_profile(profile):
    tools.display(preset.message["retrieve_user"])
    user_data = tools.get_chrome_element(profile, preset.preferences)
    if not user_data:
        tools.display(preset.message["invalid_profile"])
        exit(1)
    return chromeProfile.get_user(user_data)


def run_chrome(profile, output, refresh, undupe, clean, import_txt, get_hostname, output_name):
    print("profile[", profile,
          "]\noutput[", output,
          "]\nrefresh[", refresh,
          "]\nundupe[", undupe,
          "]\nclean[", clean,
          "]\nimport_txt[", import_txt,
          "]\nget_hostname[", get_hostname,
          "]\noutput_name[", output_name,
          "]")
    if import_txt == preset.none and profile == preset.none:
        tools.underline()
        tools.display(preset.message["missing_parameter"])
        tools.overline()
    else:
        # settings = bookMarks.Options()
        # settings.load_settings()
        tools.display(preset.new_line+preset.new_line)
        tools.underline()
        tools.display(preset.message["starting_export"])

        if profile != preset.none:
            email, full, name = get_profile(profile)
            bookmarks = bookMarks.generate_bookmarks(profile)
            tools.underline()
            tools.display(preset.message["process_user"] + ": {", full, "} [" + email + "]")
            tools.overline()
            bookmarks_data = bookMarks.generate_data(bookmarks)
        else:
            bookmarks_data = []

        if import_txt != preset.none:
            bookmarks_data = append_data_table(bookmarks_data, import_text_file(import_txt))

        if output_name == preset.none:
            if output == "xlsx":
                output_name = preset.xlsx_filename
            else:
                output_name = preset.html_filename

        if output == "xlsx":
            generate_work_book(output_name, bookmarks_data, refresh, undupe, clean, get_hostname)
        else:
            generate_web_page(output_name, bookmarks_data, refresh, undupe, clean, get_hostname)


if __name__ == "__main__":
    argument_parser = ArgumentParser(
        description=preset.message["main_description"]
    )
    argument_parser.add_argument(
        "--profile",
        "-p",
        help=preset.message["main_profile_help"],
        default=preset.none
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
        default=preset.none
    )
    argument_parser.add_argument(
        "--get_hostname",
        "-g",
        help=preset.message["main_hostname_help"],
        default=preset.off
    )
    argument_parser.add_argument(
        "--output_name",
        "-n",
        help=preset.message["main_filename_help"],
        default=preset.none
    )

    arguments = vars(argument_parser.parse_args())
    run_chrome(**arguments)
