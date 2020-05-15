import tqdm
import tools
import utils
import preset
import bookMarks

import htmlExport
import htmlSupport

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
    tools.debug("filename    [", str(web_page_filename),
                "]\nreload_title[", str(reload_url_title),
                "]\nremove_dupes[", str(remove_duplicated_urls),
                "]\nremove_track[", str(remove_tracking_from_url),
                "]\nget_hostname[", str(get_hostname_title), "]")
    tools.display(preset.message["generating_html"] + " [" + web_page_filename + "]")

    visited_hostname_title = set()
    visited_url_address = set()
    folder_list = []
    data_table_without_duplicates = []
    if remove_duplicated_urls:
        tools.underline()
        tools.display(preset.message["removing_duplicates"])
        tools.overline()
        total_items = len(data_table)
        disabled = False
        if preset.gui_progress_dialog:
            disabled = True
        with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
            utils.update_progress(preset.message["removing_duplicates"], -1, total_items)
            for index, data_row in enumerate(data_table):

                header = preset.Header()
                header.set_data(data_row)

                progress_bar.update(1)
                if utils.update_progress(preset.message["removing_duplicates"], index, total_items):
                    break

                if remove_tracking_from_url:
                    url_address = header.get_name(preset.url_clean_attr)
                else:
                    url_address = header.get_name(preset.url_attr)
                if url_address not in visited_url_address:
                    visited_url_address.add(url_address)
                    data_table_without_duplicates.append(data_row)
    else:
        data_table_without_duplicates = data_table

    tools.underline()
    tools.display(preset.message["writing_html"])
    tools.overline()
    total_items = len(data_table_without_duplicates)
    disabled = False
    if preset.gui_progress_dialog:
        disabled = True
    with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
        utils.update_progress(preset.message["writing_html"], -1, total_items)
        for index, data_row in enumerate(data_table_without_duplicates):

            header = preset.Header()
            header.set_data(data_row)

            progress_bar.update(1)
            if utils.update_progress(preset.message["writing_html"], index, total_items):
                break

            url_title = header.get_name(preset.url_name_attr)

            if remove_tracking_from_url:
                url_address = header.get_name(preset.url_clean_attr)
            else:
                url_address = header.get_name(preset.url_attr)

            hostname_title = header.get_name(preset.hostname_attr)
            original_hostname = header.get_name(preset.hostname_attr)

            if reload_url_title:
                status_number, url_title = htmlSupport.get_title(url_address)
                if status_number != 0:
                    url_title = "[ " + url_title + " " + str(status_number) + " - " + header.get_name(preset.url_name_attr) + " ]"

            if get_hostname_title:
                status_number, hostname_title = htmlSupport.get_title(preset.protocol + original_hostname)
                if status_number != 0:
                    hostname_title = "[ " + hostname_title + " " + str(status_number) + " - " + original_hostname + " ]"

            if hostname_title not in visited_hostname_title:
                url_data = tools.Urls(url_address, header.get_name(preset.url_added_attr), url_title)
                visited_hostname_title.add(hostname_title)
                folder_list.append(tools.Folder(header.get_name(preset.folder_added_attr), header.get_name(preset.folder_modified_attr), hostname_title, [url_data]))
            else:
                url_data = tools.Urls(url_address, header.get_name(preset.url_added_attr), url_title)
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
    tools.debug("filename    [", str(spreadsheet_filename),
                "]\nreload_title[", str(reload_url_title),
                "]\nremove_dupes[", str(remove_duplicated_urls),
                "]\nremove_track[", str(remove_tracking_from_url),
                "]\nget_hostname[", str(get_hostname_title), "]")
    tools.display(preset.message["generating_workbook"] + " [" + spreadsheet_filename + "]")
    excel_workbook = Workbook()
    excel_worksheet = excel_workbook.active
    excel_worksheet.title = preset.message["chrome_urls"]

    reload_url_title_disabled = True
    if reload_url_title:
        tools.underline()
        tools.display(preset.message["get_url_status"])
        tools.overline()
        reload_url_title_disabled = False

    if get_hostname_title:
        tools.underline()
        tools.display(preset.message["resolving_hostnames"])
        tools.overline()
        total_items = len(data_table)
        disabled = False
        if preset.gui_progress_dialog:
            disabled = True
        with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
            temporary_table = []
            utils.update_progress(preset.message["resolving_hostnames"], -1, total_items)
            for index, data_row in enumerate(data_table):
                temporary_table.append(utils.update_tuple(data_row, htmlSupport.get_title(preset.protocol + data_row[22])[1], 2))
                progress_bar.update(1)
                if utils.update_progress(preset.message["resolving_hostnames"], index, total_items):
                    break
            data_table = temporary_table

    visited_url_address = set()
    data_table_without_duplicates = []
    tools.display(preset.message["find_duplicated_lines"])
    total_items = len(data_table)
    disabled = False
    if reload_url_title_disabled:
        disabled = True
    elif preset.gui_progress_dialog:
        disabled = True
    with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
        utils.update_progress(preset.message["find_duplicated_lines"], -1, total_items)
        for index, data_row in enumerate(data_table):
            if utils.update_progress(preset.message["find_duplicated_lines"], index, total_items):
                break

            header = preset.Header()
            header.set_data(data_row)
            if remove_tracking_from_url:
                url_address = header.get_name(preset.url_clean_attr)
            else:
                url_address = header.get_name(preset.url_attr)

            url_name = header.get_name(preset.url_name_attr)

            if url_address not in visited_url_address:
                visited_url_address.add(url_address)
                data_table_without_duplicates.append(("MAIN", get_title_conditional(progress_bar, reload_url_title_disabled, url_name, url_address)) + data_row)
            elif not remove_duplicated_urls:
                data_table_without_duplicates.append(("DUPE", get_title_conditional(progress_bar, reload_url_title_disabled, url_name, url_address)) + data_row)

    tools.display(preset.message["writing_spreadsheet"])
    tools.overline()
    total_items = len(data_table_without_duplicates)
    disabled = False
    if preset.gui_progress_dialog:
        disabled = True
    with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
        utils.update_progress(preset.message["writing_spreadsheet"], -1, total_items)
        data_row_header = ["DUPE", "Site Name"]
        for item in preset.label_dictionary:
            data_row_header.append(preset.label_dictionary[item])
        excel_worksheet.append(tuple(data_row_header))
        for index, data_row in enumerate(data_table_without_duplicates):
            progress_bar.update(1)
            if utils.update_progress(preset.message["writing_spreadsheet"], index, total_items):
                break
            excel_worksheet.append(data_row)

    excel_worksheet.freeze_panes = "A2"
    excel_worksheet.auto_filter.ref = "A1:AU30000"

    tools.underline()
    tools.display(preset.message["format_columns"])
    tools.overline()
    font_columns = ['T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD',
                    'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN',
                    'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU']
    total_items = (len(font_columns)*len(excel_worksheet['T']))
    disabled = False
    if preset.gui_progress_dialog:
        disabled = True
    with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
        utils.update_progress(preset.message["format_columns"], -1, total_items)
        for font_column in font_columns:
            for index, worksheet_column in enumerate(excel_worksheet[font_column]):
                progress_bar.update(1)
                if utils.update_progress(preset.message["format_columns"], index, total_items):
                    break
                worksheet_column.font = Font(size=10, name='Courier New')

    tools.underline()
    tools.display(preset.message["format_dates"])
    tools.overline()
    date_columns = ['G', 'H', 'I', 'P', 'Q', 'R']
    total_items = (len(date_columns)*len(excel_worksheet['G']))
    disabled = False
    if preset.gui_progress_dialog:
        disabled = True
    with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
        utils.update_progress(preset.message["format_dates"], -1, total_items)
        for date_column in date_columns:
            excel_worksheet.column_dimensions[date_column].width = 18
            for index, worksheet_column in enumerate(excel_worksheet[date_column]):
                progress_bar.update(1)
                if utils.update_progress(preset.message["format_dates"], index, total_items):
                    break
                worksheet_column.number_format = preset.number_format

    tools.underline()
    tools.display(preset.message["hide_columns"])
    hidden_columns = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'AA', 'AB', 'AC', 'AD']
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
    return tools.get_user(user_data)


def run_chrome(profile, output, refresh, undupe, clean, import_txt, get_hostname, output_name, list_profile, x_org_gui):
    tools.debug("profile       [", str(profile),
                "]\noutput        [", str(output),
                "]\nrefresh       [", str(refresh),
                "]\nundupe        [", str(undupe),
                "]\nclean         [", str(clean),
                "]\nimport_txt    [", str(import_txt),
                "]\nget_hostname  [", str(get_hostname),
                "]\noutput_name   [", str(output_name),
                "]\nlist_profiles [" + str(list_profile) + "]")
    if x_org_gui:
        import chromeExport
        chromeExport.main()
    elif list_profile:
        if not list_profile.isdigit():
            list_profile = preset.all_profiles
        tools.list_profiles(list_profile)
    else:
        if import_txt == preset.none and profile == preset.none:
            tools.underline()
            tools.display(preset.message["missing_parameter"])
            tools.overline()
        else:
            tools.display(preset.new_line+preset.new_line)
            tools.underline()
            tools.display(preset.message["starting_export"])

            if profile:
                email, full, name = get_profile(profile)
                bookmarks = bookMarks.generate_bookmarks(profile)
                tools.underline()
                tools.display(preset.message["process_user"] + ": {", full, "} [" + email + "]")
                tools.overline()
                bookmarks_data = bookMarks.generate_data(bookmarks)
            else:
                bookmarks_data = []

            if import_txt:
                bookmarks_data = append_data_table(bookmarks_data, import_text_file(import_txt))

            if not output_name:
                if output == "xlsx":
                    output_name = preset.xlsx_filename
                else:
                    output_name = preset.html_filename

            refresh = normalize(refresh)
            undupe = normalize(undupe)
            clean = normalize(clean)
            get_hostname = normalize(get_hostname)

            if output == "xlsx":
                generate_work_book(output_name, bookmarks_data, refresh, undupe, clean, get_hostname)
            else:
                generate_web_page(output_name, bookmarks_data, refresh, undupe, clean, get_hostname)


def normalize(parameter):
    if parameter == preset.on or parameter == preset.true:
        return True
    return False


def default(default_value):
    if default_value:
        return preset.message["enabled"]
    return preset.message["disabled"]


if __name__ == "__main__":
    settings = bookMarks.Options()
    settings.load_settings()

    default_output = "xlsx"
    if settings.export_file_type:
        default_output = "html"

    argument_parser = ArgumentParser(
        description=preset.message["main_description"]
    )
    argument_parser.add_argument(
        "-p",
        dest='profile',
        help=preset.message["main_profile_help"],
        default=preset.none
    )
    argument_parser.add_argument(
        "-o",
        dest='output',
        help=preset.message["main_output_help"] + preset.message["default"] + default_output + ".",
        default=default_output
    )
    argument_parser.add_argument(
        "-r",
        dest='refresh',
        help=preset.message["main_refresh_help"] + preset.message["default"] + default(settings.refresh_url_title),
        nargs="?",
        const=preset.true,
        default=settings.refresh_url_title
    )
    argument_parser.add_argument(
        "-u",
        dest='undupe',
        help=preset.message["main_undupe_help"] + preset.message["default"] + default(settings.remove_duplicated_urls),
        nargs="?",
        const=preset.true,
        default=settings.remove_duplicated_urls
    )
    argument_parser.add_argument(
        "-c",
        dest='clean',
        help=preset.message["main_clean_help"] + preset.message["default"] + default(settings.remove_tracking_tokens_from_url),
        nargs="?",
        const=preset.true,
        default=settings.remove_tracking_tokens_from_url
    )
    argument_parser.add_argument(
        "-i",
        dest='import_txt',
        help=preset.message["main_import_help"],
        default=preset.none
    )
    argument_parser.add_argument(
        "-g",
        dest='get_hostname',
        help=preset.message["main_hostname_help"] + preset.message["default"] + default(settings.refresh_folder_name_with_hostname_title),
        nargs="?",
        const=preset.true,
        default=settings.refresh_folder_name_with_hostname_title
    )
    argument_parser.add_argument(
        "-n",
        dest="output_name",
        help=preset.message["main_filename_help"],
        default=preset.none
    )
    argument_parser.add_argument(
        "-l",
        dest="list_profile",
        help=preset.message["profile_help"] + preset.message["default"] + preset.message["all_profiles"],
        nargs="?",
        const=preset.all_profiles
    )
    argument_parser.add_argument(
        "-x",
        dest='x_org_gui',
        help=preset.message["open_gui"],
        action='store_true'
    )
    arguments = vars(argument_parser.parse_args())
    run_chrome(**arguments)
