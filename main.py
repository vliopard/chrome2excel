import tools
import preset
import database
import bookmarks
import html_export
import pandas as pd

import logging
show = logging.getLogger(preset.MAIN_SECTION)

test = True
reset = False
dedupe = True

URL_TITLE = 'url_info_name'
URL_CLEAN = 'url_info_parse_address'
URL_ORIGINAL = 'url_info_prime_address'
URL_CREATED = 'url_info_date_added'
FOLDER_NAME = 'folder_info_name_proposal'
FOLDER_CREATED = 'folder_info_date_added'
FOLDER_MODIFIED = 'folder_info_date_modified'
URL_DOMAIN = 'url_data_fld'


if __name__ == '__main__':
    bookmarks_data = bookmarks.generate_data(bookmarks.generate_bookmarks(3))

    print('Sorting data...')
    sorted_bookmarks = sorted(bookmarks_data, key=lambda v: (v[URL_DOMAIN], v[URL_CLEAN], v[URL_TITLE]))

    sorted_bookmarks_length = len(sorted_bookmarks)
    print(f'TOTAL BRUTE [{sorted_bookmarks_length:,}]')

    url_number = 0
    if dedupe:
        bookmarks_list = []
        bookmarks_data_dedupe = set()

        print('Removing duplicates...')  # TODO: SAVE A BACKUP WITHOUT REMOVING DUPLICATES BEFORE APPLY TO CHROME
        for bookmark_item in sorted_bookmarks:
            # main_url = bookmark_item[URL_CLEAN].strip()
            main_url = bookmark_item['url_info_undup_address']
            if main_url and main_url not in bookmarks_data_dedupe:
                bookmarks_data_dedupe.add(main_url)
                url_number += 1
                url_dictionary = {
                    'folder_info_date_added': bookmark_item['folder_info_date_added'],
                    'folder_info_date_modified': bookmark_item['folder_info_date_modified'],
                    'folder_info_name_proposal': bookmark_item['folder_info_name_proposal'],
                    'url_data_fld': bookmark_item['url_data_fld'],
                    'url_info_date_added': bookmark_item['url_info_date_added'],
                    'url_info_name': bookmark_item['url_info_name'],
                    'url_info_parse_address': bookmark_item['url_info_parse_address'],
                    'url_info_prime_address': bookmark_item['url_info_prime_address']
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
        url_name = bookmark_element[URL_TITLE]
        url_data = tools.Urls(bookmark_element[URL_CLEAN], bookmark_element[URL_CREATED], url_name)
        if bookmark_element[FOLDER_NAME] not in visited_hostname_title:
            visited_hostname_title.add(bookmark_element[FOLDER_NAME])
            folder_list.append(tools.Folder(bookmark_element[FOLDER_CREATED], bookmark_element[FOLDER_MODIFIED], bookmark_element[FOLDER_NAME], [url_data]))
            directory_count += 1
            url_count += 1
        else:
            for folder in folder_list:
                if folder.folder_name == bookmark_element[FOLDER_NAME]:
                    folder.add_url(url_data)
                    url_count += 1

    print(f'DIRS [{directory_count:,}] LINKS [{url_count:,}]')
    print('Convert to HTML...')
    html_export.write_html('output.html', folder_list)
    print('Convert to DataFrame...')
    pandas_dataframe = pd.DataFrame(bookmarks_list)
    print('Convert to XLSX...')
    pandas_dataframe.to_excel('output.xlsx', index=False)

    print('Done.')
