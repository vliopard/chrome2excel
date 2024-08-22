import tools
import preset
import database
import bookmarks
import html_export
import pandas as pd


if __name__ == preset.__MAIN__:
    DEDUPE_LINKS = True
    preset.CLEAN_URL_BOOL = True
    preset.REFRESH_TITLE = False
    preset.DIRECTORY_SUGGESTION = True
    bookmarks_data = bookmarks.generate_data(bookmarks.generate_bookmarks(3))

    print(preset.TEXT_SORTING_DATA)
    if preset.DIRECTORY_SUGGESTION:
        sorted_bookmarks = sorted(bookmarks_data, key=lambda v: (v[preset.URL_DATA_FLD], v[preset.URL_CLEAN], v[preset.URL_TITLE]))
    else:
        sorted_bookmarks = sorted(bookmarks_data, key=lambda v: (v[preset.URL_CLEAN], v[preset.URL_TITLE]))

    sorted_bookmarks_length = len(sorted_bookmarks)
    print(f'TOTAL BRUTE [{sorted_bookmarks_length:,}]')

    url_number = 0
    if DEDUPE_LINKS:
        bookmarks_list = []
        bookmarks_data_dedupe = set()

        print(preset.TEXT_REMOVING_DUPLICATES)
        for bookmark_item in sorted_bookmarks:            
            main_url = bookmark_item[preset.URL_INFO_UNDUP_ADDRESS]
            if main_url and main_url not in bookmarks_data_dedupe:
                bookmarks_data_dedupe.add(main_url)
                url_number += 1

                if preset.DIRECTORY_SUGGESTION:
                    folder_name = preset.FOLDER_INFO_NAME_PROPOSAL
                    folder_domain = preset.URL_DATA_FLD
                else:
                    folder_name = preset.FOLDER_INFO_NAME
                    folder_domain = preset.URL_DATA_NETLOC

                url_dictionary = {
                    preset.FOLDER_INFO_DATE_ADDED: bookmark_item[preset.FOLDER_INFO_DATE_ADDED],
                    preset.FOLDER_INFO_DATE_MODIFIED: bookmark_item[preset.FOLDER_INFO_DATE_MODIFIED],
                    folder_name: bookmark_item[folder_name],
                    folder_domain: bookmark_item[folder_domain],
                    preset.URL_INFO_DATE_ADDED: bookmark_item[preset.URL_INFO_DATE_ADDED],
                    preset.URL_INFO_NAME: bookmark_item[preset.URL_INFO_NAME],
                    preset.URL_INFO_NAME_PREVIOUS: bookmark_item[preset.URL_INFO_NAME_PREVIOUS],
                    preset.URL_INFO_PARSE_ADDRESS: bookmark_item[preset.URL_INFO_PARSE_ADDRESS],
                    preset.URL_INFO_PRIME_ADDRESS: bookmark_item[preset.URL_INFO_PRIME_ADDRESS]
                }
                bookmarks_list.append(url_dictionary)
                database.insert_url(url_dictionary)
    else:
        bookmarks_list = sorted_bookmarks

    print(f'TOTAL PRIME [{url_number:,}]')
    folder_list = []

    directory_count = 0
    url_count = 0

    visited_hostname_title = set()
    for bookmark_element in bookmarks_list:
        url_name = bookmark_element[preset.URL_TITLE]
        url_data = tools.Urls(bookmark_element[preset.URL_CLEAN], bookmark_element[preset.URL_CREATED], url_name)

        if preset.DIRECTORY_SUGGESTION:
            used_folder = preset.FOLDER_NAME
        else:
            used_folder = preset.FOLDER_INFO_NAME

        if bookmark_element[used_folder] not in visited_hostname_title:
            visited_hostname_title.add(bookmark_element[used_folder])
            folder_list.append(tools.Folder(bookmark_element[preset.FOLDER_CREATED], bookmark_element[preset.FOLDER_MODIFIED], bookmark_element[used_folder], [url_data]))
            directory_count += 1
            url_count += 1
        else:
            for folder in folder_list:
                if folder.folder_name == bookmark_element[used_folder]:
                    folder.add_url(url_data)
                    url_count += 1

    print(f'DIRS [{directory_count:,}] LINKS [{url_count:,}]')
    print(preset.TEXT_CONVERT_TO_HTML)
    html_export.write_html(preset.OUTPUT_HTML, folder_list)
    print(preset.TEXT_CONVERT_TO_DATAFRAME)
    pandas_dataframe = pd.DataFrame(bookmarks_list)
    print(preset.TEXT_CONVERT_TO_XLSX)
    pandas_dataframe.to_excel(preset.OUTPUT_XLSX, index=False)

    print(preset.TEXT_DONE)
