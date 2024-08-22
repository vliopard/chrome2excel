import tqdm
import tools
import utils
import preset
import bookmarks
import html_export
import title_master
import html_support

from openpyxl import Workbook
from openpyxl.styles import Font

from argparse import ArgumentParser


def get_title_conditional(progress_bar, paramz, url_name, url_address):
    progress_bar.update(1)
    if paramz[preset.COMMAND_REFRESH_URL_TITLE]:
        return title_master.get_title_master(url_address)
    return url_name


def import_text_file(text_file=preset.TEXT_FILENAME):
    tools.print_box(f'{preset.MESSAGE[preset.IMPORT_TEXT_FILE]} [{text_file}]')
    url_list = []
    with open(text_file, encoding=preset.CHARSET_UTF8) as text_file:
        for url_item in text_file:
            url_list.append(url_item.strip())
    return url_list


def append_data_table(data_table, url_list):
    tools.print_display(preset.MESSAGE[preset.APPENDING_DATA_TABLE])
    for url_item in url_list:
        head = preset.Header()
        head.set_data(url_item)
        head.Hostname = html_support.parse_url(url_item.hostname)
        head.URL_Clean = html_support.parse_url_clean(url_item.parse)
        head.URL = url_item.url
        data_table.append(head.to_dict())
    return data_table


def generate_from_txt(url_list):
    tools.print_display(preset.MESSAGE[preset.GENERATING_FROM_TEXT])
    return append_data_table([], url_list)


def generate_web_page(data_table, paramz):
    xlsx, web_page_filename = paramz[preset.OUTPUT_NAME]
    if not xlsx and data_table:
        tools.print_display(f'{preset.MESSAGE[preset.GENERATING_HTML]} [{web_page_filename}]')
        visited_url_address = set()
        visited_hostname_title = set()
        folder_list = []
        data_table_without_duplicates = []
        if paramz[preset.UNDUPE]:
            tools.print_box(preset.MESSAGE[preset.REMOVING_DUPLICATES_VALUE])
            total_items = len(data_table)
            preset.PROGRESS_BAR_DISABLED = False
            if preset.GUI_PROGRESS_DIALOG:
                preset.PROGRESS_BAR_DISABLED = True
            with tqdm.tqdm(total=total_items, disable=preset.PROGRESS_BAR_DISABLED) as progress_bar:
                utils.update_progress(preset.MESSAGE[preset.REMOVING_DUPLICATES_VALUE], -1, total_items)
                for index, data_row in enumerate(data_table):
                    progress_bar.update(1)
                    if utils.update_progress(preset.MESSAGE[preset.REMOVING_DUPLICATES_VALUE], index, total_items):
                        break

                    if paramz[preset.COMMAND_CLEAN_URL_FROM_TRACKING]:
                        url_address = html_support.parse_url_clean(data_row[preset.URL_INFO_PRIME_ADDRESS])
                    else:
                        url_address = data_row[preset.URL_INFO_PRIME_ADDRESS]

                    if url_address not in visited_url_address:
                        visited_url_address.add(url_address)
                        data_table_without_duplicates.append(data_row)
        else:
            data_table_without_duplicates = data_table

        tools.print_box(preset.MESSAGE[preset.WRITING_HTML])
        total_items = len(data_table_without_duplicates)
        preset.PROGRESS_BAR_DISABLED = False
        if preset.GUI_PROGRESS_DIALOG:
            preset.PROGRESS_BAR_DISABLED = True
        with tqdm.tqdm(total=total_items, disable=preset.PROGRESS_BAR_DISABLED) as progress_bar:
            utils.update_progress(preset.MESSAGE[preset.WRITING_HTML], -1, total_items)
            for index, data_row in enumerate(data_table_without_duplicates):
                progress_bar.update(1)
                if utils.update_progress(preset.MESSAGE[preset.WRITING_HTML], index, total_items):
                    break

                url_title = data_row[preset.URL_INFO_NAME]

                if paramz[preset.COMMAND_CLEAN_URL_FROM_TRACKING]:
                    url_address = html_support.parse_url_clean(data_row[preset.URL_INFO_PRIME_ADDRESS])
                else:
                    url_address = data_row[preset.URL_INFO_PRIME_ADDRESS]

                hostname_title = data_row[preset.FOLDER_INFO_NAME]

                if paramz[preset.COMMAND_REFRESH_URL_TITLE]:
                    url_title = title_master.get_title_master(url_address)

                if paramz[preset.COMMAND_REFRESH_FOLDER_NAME]:
                    preset.DIRECTORY_SUGGESTION = True
                    hostname_title = html_support.parse_url(data_row[preset.URL_INFO_PRIME_ADDRESS])[preset.FOLDER_INFO_NAME_PROPOSAL]

                if hostname_title not in visited_hostname_title:
                    url_data = tools.Urls(url_address, data_row[preset.URL_INFO_DATE_ADDED], url_title)
                    visited_hostname_title.add(hostname_title)
                    folder_list.append(tools.Folder(data_row[preset.FOLDER_INFO_DATE_ADDED], data_row[preset.FOLDER_INFO_DATE_MODIFIED], hostname_title, [url_data]))
                else:
                    url_data = tools.Urls(url_address, data_row[preset.URL_INFO_DATE_ADDED], url_title)
                    for folder in folder_list:
                        if folder.folder_name == hostname_title:
                            folder.add_url(url_data)

        tools.print_box(preset.MESSAGE[preset.SAVING_HTML])
        html_export.write_html(web_page_filename, folder_list)
        tools.print_display(preset.MESSAGE[preset.DONE])
        tools.print_overline()


def generate_work_book(data_table, paramz):
    xlsx, spreadsheet_filename = paramz[preset.OUTPUT_NAME]
    if xlsx and data_table:
        tools.print_display(f'{preset.MESSAGE[preset.GENERATING_WORKBOOK]} [{spreadsheet_filename}]')

        excel_workbook = Workbook()
        excel_worksheet = excel_workbook.active
        excel_worksheet.title = preset.MESSAGE[preset.CHROME_URLS]

        if paramz[preset.COMMAND_REFRESH_URL_TITLE]:
            tools.print_box(preset.MESSAGE[preset.GET_URL_STATUS])

        if paramz[preset.COMMAND_REFRESH_FOLDER_NAME]:
            tools.print_box(preset.MESSAGE[preset.RESOLVING_HOSTNAMES])
            total_items = len(data_table)
            preset.PROGRESS_BAR_DISABLED = False
            if preset.GUI_PROGRESS_DIALOG:
                preset.PROGRESS_BAR_DISABLED = True
            with tqdm.tqdm(total=total_items, disable=preset.PROGRESS_BAR_DISABLED) as progress_bar:
                temporary_table = []
                utils.update_progress(preset.MESSAGE[preset.RESOLVING_HOSTNAMES], -1, total_items)
                for index, data_row in enumerate(data_table):
                    preset.DIRECTORY_SUGGESTION = True
                    data_row[preset.FOLDER_INFO_NAME] = html_support.parse_url(data_row[preset.URL_INFO_PRIME_ADDRESS])[preset.FOLDER_INFO_NAME_PROPOSAL]
                    temporary_table.append(data_row)
                    progress_bar.update(1)
                    if utils.update_progress(preset.MESSAGE[preset.RESOLVING_HOSTNAMES], index, total_items):
                        break
                data_table = temporary_table

        visited_url_address = set()
        data_table_without_duplicates = []
        tools.print_display(preset.MESSAGE[preset.FIND_DUPLICATED_LINES])
        total_items = len(data_table)
        preset.PROGRESS_BAR_DISABLED = False
        if paramz[preset.COMMAND_REFRESH_URL_TITLE]:
            preset.PROGRESS_BAR_DISABLED = True
        elif preset.GUI_PROGRESS_DIALOG:
            preset.PROGRESS_BAR_DISABLED = True

        with tqdm.tqdm(total=total_items, disable=preset.PROGRESS_BAR_DISABLED) as progress_bar:
            utils.update_progress(preset.MESSAGE[preset.FIND_DUPLICATED_LINES], -1, total_items)
            for index, data_row in enumerate(data_table):
                if utils.update_progress(preset.MESSAGE[preset.FIND_DUPLICATED_LINES], index, total_items):
                    break

                if paramz[preset.COMMAND_CLEAN_URL_FROM_TRACKING]:
                    data_row[preset.URL_INFO_PARSE_ADDRESS] = html_support.parse_url_clean(data_row[preset.URL_INFO_PRIME_ADDRESS])
                    url_address = data_row[preset.URL_INFO_PARSE_ADDRESS]
                else:
                    url_address = data_row[preset.URL_INFO_PRIME_ADDRESS]

                dedupe_type = preset.SYMBOL_EMPTY
                if url_address not in visited_url_address:
                    visited_url_address.add(url_address)
                    dedupe_type = preset.MAIN
                elif not paramz[preset.UNDUPE]:
                    dedupe_type = preset.DUPE
                data_row[preset.URL_DEDUP_STATUS] = dedupe_type
                data_row[preset.URL_INFO_NAME] = get_title_conditional(progress_bar, paramz, data_row[preset.URL_INFO_NAME], url_address)
                data_table_without_duplicates.append(data_row)

        tools.print_display(preset.MESSAGE[preset.WRITING_SPREADSHEET])
        tools.print_overline()
        total_items = len(data_table_without_duplicates)
        preset.PROGRESS_BAR_DISABLED = False
        if preset.GUI_PROGRESS_DIALOG:
            preset.PROGRESS_BAR_DISABLED = True
        with tqdm.tqdm(total=total_items, disable=preset.PROGRESS_BAR_DISABLED) as progress_bar:
            utils.update_progress(preset.MESSAGE[preset.WRITING_SPREADSHEET], -1, total_items)

            values = []
            preset.DICTIONARY_STRUCTURE.pop(preset.FOLDER_INFO_NAME_PROPOSAL, None)
            preset.DICTIONARY_STRUCTURE.pop(preset.URL_DATA_FLD, None)
            for key in preset.DICTIONARY_STRUCTURE:
                values.append(key)
            values.append(preset.TERM)
            excel_worksheet.append(values)

            for index, data_row in enumerate(data_table_without_duplicates):
                progress_bar.update(1)
                if utils.update_progress(preset.MESSAGE[preset.WRITING_SPREADSHEET], index, total_items):
                    break

                spreadsheet_row = []
                for key in values:
                    if key in data_row:
                        spreadsheet_row.append(data_row[key])
                spreadsheet_row.append(preset.TERM)
                excel_worksheet.append(spreadsheet_row)

        excel_worksheet.freeze_panes = 'A2'
        excel_worksheet.auto_filter.ref = 'A1:BA90000'

        tools.print_box(preset.MESSAGE[preset.FORMAT_COLUMNS])

        date_columns = ['F', 'G', 'H', 'O', 'P', 'Q']
        font_columns = ['B', 'K', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']
        hidden_columns = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'P', 'Q', 'V', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']

        date_items_count = 'A'
        font_items_count = 'T'

        parse_column_size = 'R'
        prime_column_size = 'S'
        title_column_size = 'U'

        total_items = (len(font_columns)*len(excel_worksheet[font_items_count]))
        preset.PROGRESS_BAR_DISABLED = False
        if preset.GUI_PROGRESS_DIALOG:
            preset.PROGRESS_BAR_DISABLED = True
        with tqdm.tqdm(total=total_items, disable=preset.PROGRESS_BAR_DISABLED) as progress_bar:
            utils.update_progress(preset.MESSAGE[preset.FORMAT_COLUMNS], -1, total_items)
            for font_column in font_columns:
                for index, worksheet_column in enumerate(excel_worksheet[font_column]):
                    progress_bar.update(1)
                    if utils.update_progress(preset.MESSAGE[preset.FORMAT_COLUMNS], index, total_items):
                        break
                    worksheet_column.font = Font(size=10, name=preset.FONT_COURIER_NEW)

        tools.print_box(preset.MESSAGE[preset.FORMAT_DATES])
        total_items = (len(date_columns)*len(excel_worksheet[date_items_count]))
        disabled = False
        if preset.GUI_PROGRESS_DIALOG:
            disabled = True
        with tqdm.tqdm(total=total_items, disable=disabled) as progress_bar:
            utils.update_progress(preset.MESSAGE[preset.FORMAT_DATES], -1, total_items)
            for date_column in date_columns:
                excel_worksheet.column_dimensions[date_column].width = 18
                for index, worksheet_column in enumerate(excel_worksheet[date_column]):
                    progress_bar.update(1)
                    if utils.update_progress(preset.MESSAGE[preset.FORMAT_DATES], index, total_items):
                        break
                    worksheet_column.number_format = preset.NUMBER_FORMAT

        tools.print_underline()
        tools.print_display(preset.MESSAGE[preset.HIDE_COLUMNS])
        for h in hidden_columns:
            excel_worksheet.column_dimensions[h].width = 9
            excel_worksheet.column_dimensions[h].hidden = True

        tools.print_display(preset.MESSAGE[preset.FORMAT_HEADER])
        for cell in excel_worksheet['1:1']:
            cell.font = Font(bold=True)

        tools.print_display(preset.MESSAGE[preset.SIZING_COLUMNS])
        excel_worksheet.column_dimensions[title_column_size].width = 30
        excel_worksheet.column_dimensions[parse_column_size].width = 85
        excel_worksheet.column_dimensions[prime_column_size].width = 85
        excel_worksheet.column_dimensions[font_items_count].width = 85

        tools.print_display(preset.MESSAGE[preset.SAVING_WORKBOOK])
        excel_workbook.save(spreadsheet_filename)
        tools.print_display(preset.MESSAGE[preset.DONE])
        tools.print_overline()


def get_profile(profile):
    tools.print_display(preset.MESSAGE[preset.RETRIEVE_USER])
    user_data = tools.get_chrome_element(profile, preset.PREFERENCES)
    if not user_data:
        tools.print_display(preset.MESSAGE[preset.INVALID_PROFILE])
        exit(1)
    return tools.get_user(user_data)


def show_debug_params(dic_parameters):
    display_dic = ''
    for key in dic_parameters:
        display_dic += f'{key.ljust(15)}[{str(dic_parameters[key]).ljust(6)}]{preset.NEW_LINE}'
    tools.print_debug(display_dic)


def start_gui(dic_parameters):
    if dic_parameters[preset.X_ORG_GUI]:
        import chrome_export
        chrome_export.main()
        exit(0)


def list_profiles(dic_parameters):
    if dic_parameters[preset.LIST_PROFILE]:
        if dic_parameters[preset.LIST_PROFILE].isdigit():
            list_profile = dic_parameters[preset.LIST_PROFILE]
        else:
            list_profile = preset.PROFILES
        tools.list_profiles(list_profile)
        return False
    else:
        return True


def run_chrome(dic_parameters):
    show_debug_params(dic_parameters)
    start_gui(dic_parameters)

    if list_profiles(dic_parameters):
        if dic_parameters[preset.IMPORT_TXT] == preset.NONE and dic_parameters[preset.PROFILE] == preset.NONE:
            tools.print_box(preset.MESSAGE[preset.MISSING_PARAMETER])
            return

        tools.print_display(f'{preset.NEW_LINE}{preset.NEW_LINE}')
        tools.print_underline()
        tools.print_display(preset.MESSAGE[preset.STARTING_EXPORT])

        bookmarks_data = []
        if dic_parameters[preset.PROFILE]:
            email, full, name = get_profile(dic_parameters[preset.PROFILE])
            tools.print_box(f'{preset.MESSAGE[preset.PROCESS_USER]}: ({full}) [{email}]')
            bookmarks_data = bookmarks.generate_data(bookmarks.generate_bookmarks(dic_parameters[preset.PROFILE]))

        if dic_parameters[preset.IMPORT_TXT]:
            bookmarks_data = append_data_table(bookmarks_data, import_text_file(dic_parameters[preset.IMPORT_TXT]))

        generate_work_book(bookmarks_data, dic_params(dic_parameters))
        generate_web_page(bookmarks_data, dic_params(dic_parameters))


def dic_params(dic_parameters):
    return {
        preset.OUTPUT_NAME: out_name(dic_parameters),
        preset.COMMAND_REFRESH_URL_TITLE: normalize(dic_parameters[preset.COMMAND_REFRESH_URL_TITLE]),
        preset.UNDUPE: normalize(dic_parameters[preset.UNDUPE]),
        preset.COMMAND_CLEAN_URL_FROM_TRACKING: normalize(dic_parameters[preset.COMMAND_CLEAN_URL_FROM_TRACKING]),
        preset.COMMAND_REFRESH_FOLDER_NAME: normalize(dic_parameters[preset.COMMAND_REFRESH_FOLDER_NAME])
    }


def out_name(dic_parameters):
    xlsx = False
    if dic_parameters[preset.OUTPUT_NAME]:
        output_name = dic_parameters[preset.OUTPUT_NAME]
    else:
        if dic_parameters[preset.OUTPUT] == preset.XLSX:
            xlsx = True
            output_name = preset.XLSX_FILENAME
        else:
            output_name = preset.HTML_FILENAME
    return xlsx, output_name


def normalize(parameter):
    return parameter == preset.ON or parameter == preset.TRUE


def default(default_value):
    return preset.MESSAGE[preset.ENABLED if default_value else preset.DISABLED]


if __name__ == preset.__MAIN__:
    settings = bookmarks.Options()
    settings.load_settings()
    default_output = preset.XLSX if settings.export_file_type else preset.HTML

    argument_parser = ArgumentParser(description=preset.MESSAGE[preset.MAIN_DESCRIPTION])

    argument_parser.add_argument('-p', dest=preset.PROFILE,
                                 help=preset.MESSAGE[preset.MAIN_PROFILE_HELP],
                                 default=preset.NONE)
    argument_parser.add_argument('-o', dest=preset.OUTPUT,
                                 help=f'{preset.MESSAGE[preset.MAIN_OUTPUT_HELP]}{preset.MESSAGE[preset.DEFAULT_L]}{default_output}.',
                                 default=default_output)
    argument_parser.add_argument('-r', dest=preset.COMMAND_REFRESH_URL_TITLE,
                                 help=f'{preset.MESSAGE[preset.MAIN_REFRESH_HELP]}{preset.MESSAGE[preset.DEFAULT_L]}{default(settings.refresh_url_title)}',
                                 nargs=preset.SYMBOL_QM,
                                 const=preset.TRUE,
                                 default=settings.refresh_url_title)
    argument_parser.add_argument('-u', dest=preset.UNDUPE,
                                 help=f'{preset.MESSAGE[preset.MAIN_UNDUPE_HELP]}{preset.MESSAGE[preset.DEFAULT_L]}{default(settings.remove_duplicated_urls)}',
                                 nargs=preset.SYMBOL_QM,
                                 const=preset.TRUE,
                                 default=settings.remove_duplicated_urls)
    argument_parser.add_argument('-c', dest=preset.COMMAND_CLEAN_URL_FROM_TRACKING,
                                 help=f'{preset.MESSAGE[preset.MAIN_CLEAN_HELP]}{preset.MESSAGE[preset.DEFAULT_L]}{default(settings.remove_tracking_tokens_from_url)}',
                                 nargs=preset.SYMBOL_QM,
                                 const=preset.TRUE,
                                 default=settings.remove_tracking_tokens_from_url)
    argument_parser.add_argument('-i', dest=preset.IMPORT_TXT,
                                 help=preset.MESSAGE[preset.MAIN_IMPORT_HELP],
                                 default=preset.NONE)
    argument_parser.add_argument('-g', dest=preset.COMMAND_REFRESH_FOLDER_NAME,
                                 help=f'{preset.MESSAGE[preset.MAIN_HOSTNAME_HELP]}{preset.MESSAGE[preset.DEFAULT_L]}{default(settings.refresh_folder_name_with_hostname_title)}',
                                 nargs=preset.SYMBOL_QM,
                                 const=preset.TRUE,
                                 default=settings.refresh_folder_name_with_hostname_title)
    argument_parser.add_argument('-n', dest=preset.OUTPUT_NAME,
                                 help=preset.MESSAGE[preset.MAIN_FILENAME_HELP],
                                 default=preset.NONE)
    argument_parser.add_argument('-l', dest=preset.LIST_PROFILE,
                                 help=f'{preset.MESSAGE[preset.PROFILE_HELP]}{preset.MESSAGE[preset.DEFAULT_L]}{preset.MESSAGE[preset.ALL_PROFILES]}',
                                 nargs=preset.SYMBOL_QM,
                                 const=preset.PROFILES)
    argument_parser.add_argument('-x', dest=preset.X_ORG_GUI,
                                 help=preset.MESSAGE[preset.OPEN_GUI],
                                 action=preset.STORE_TRUE)
    run_chrome(vars(argument_parser.parse_args()))
