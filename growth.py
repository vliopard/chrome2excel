import sys
import preset
from tqdm import tqdm
from time import sleep
from pymongo import MongoClient

mongo_client = MongoClient(preset.DATABASE_URL)
mongo_database = mongo_client[preset.DATABASE_NAME]
mongo_collection = mongo_database[preset.DATABASE_COLLECTION]
mongo_collection_names = mongo_database[preset.DATABASE_COLLECTION_NAMES]
mongo_collection_folders = mongo_database[preset.DATABASE_COLLECTION_FOLDERS]

if __name__ == "__main__":
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
            tqdm_progress_bar.refresh()
            sleep(60)
