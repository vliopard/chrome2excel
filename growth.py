import os
import sys
import preset
from tqdm import tqdm
from pymongo import MongoClient
from time import sleep, time, strftime, localtime

mongo_client = MongoClient(preset.DATABASE_URL)
mongo_database = mongo_client[preset.DATABASE_NAME]
mongo_collection = mongo_database[preset.DATABASE_COLLECTION]
mongo_collection_names = mongo_database[preset.DATABASE_COLLECTION_NAMES]
mongo_collection_folders = mongo_database[preset.DATABASE_COLLECTION_FOLDERS]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == preset.__MAIN__:
    clear_screen()
    # directories = mongo_collection_folders.count_documents({})
    links = mongo_collection.count_documents({})
    url_names = mongo_collection_names.count_documents({})

    print('URL Scan in progress...')
    status_bar_format = "{desc}: {percentage:.2f}%|{bar}| {n:,}/{total:,} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
    with tqdm(total=links, bar_format=status_bar_format, file=sys.stdout) as tqdm_progress_bar:
        for number in range(url_names):
            tqdm_progress_bar.update(1)

        new_range = links - url_names
        for value in range(new_range):
            url_name = mongo_collection_names.count_documents({})
            new_url = url_name - url_names
            if new_url > 0:
                tqdm_progress_bar.update(new_url)
                url_names = url_name


            elapsed = tqdm_progress_bar.format_dict["elapsed"]
            rate = tqdm_progress_bar.format_dict["rate"]
            etf = (tqdm_progress_bar.total - tqdm_progress_bar.n) / rate if rate and tqdm_progress_bar.total else 0

            #etf = tqdm_progress_bar.format_dict['remaining']
            now = time()
            now_plus_etf = now + etf
            cdir = strftime('%Y/%m/%d %H:%M:%S', localtime(now_plus_etf))

            tqdm_progress_bar.set_postfix({'ETF': cdir})
            tqdm_progress_bar.refresh()
            sleep(60)
