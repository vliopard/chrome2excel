import json
import preset
import argparse
from tqdm import tqdm
from tools import timed
from tools import section_line
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

refresh_collections = False

mongo_client = MongoClient(preset.DATABASE_URL)
mongo_database = mongo_client[preset.DATABASE_NAME]

mongo_collection = mongo_database[preset.DATABASE_COLLECTION]
mongo_collection_names = mongo_database[preset.DATABASE_COLLECTION_NAMES]
mongo_collection_folders = mongo_database[preset.DATABASE_COLLECTION_FOLDERS]

mongo_stats = mongo_database[preset.DATABASE_STATUS]


@timed
def duplicate_collection(collection_name):
    if collection_name.startswith(preset.DATABASE_COLLECTION):
        new_collection = mongo_database[collection_name]
        new_collection.insert_many(mongo_collection.find())
        return
    if collection_name.startswith(preset.DATABASE_COLLECTION_NAMES):
        new_collection = mongo_database[collection_name]
        new_collection.insert_many(mongo_collection_names.find())
        return
    if collection_name.startswith(preset.DATABASE_COLLECTION_FOLDERS):
        new_collection = mongo_database[collection_name]
        new_collection.insert_many(mongo_collection_folders.find())
        return
    print(f'No collection to duplicate {collection_name}')


def get_db_size(collection_name):
    collection_cursor = mongo_database[collection_name]
    stats = mongo_database.command("collstats", collection_name)
    return {preset.DATABASE_ID: collection_name, 'size': stats['size'], 'count': collection_cursor.count_documents({})}


@timed
def list_collections(size):
    if refresh_collections:
        mongo_stats.delete_many({})

    collection_list = mongo_database.list_collection_names()

    si = mongo_client.server_info()
    operating_system = si['targetMinOS']

    print(f'LIST OF COLLECTIONS: [{operating_system}]')
    print(f'{section_line(preset.SYMBOL_UNDERLINE, preset.LINE_LEN)}')
    for collection_name in sorted(collection_list):
        if collection_name == preset.DATABASE_STATUS:
            continue
        if size:
            stats_db = get_status(collection_name)
            if not stats_db:
                add_status_item = get_db_size(collection_name)
                size_bytes = add_status_item['size']
                count = add_status_item['count']
                add_status(add_status_item)
            else:
                size_bytes = stats_db['size']
                count = stats_db['count']
            size_bytes_str = f'{size_bytes:,}'
            count_str = f'{count:,}'

            print(f'{preset.DATABASE_NAME}:[ {collection_name.rjust(30)} ] [{count_str.rjust(9)}] [{size_bytes_str.rjust(13)}]')
        else:
            print(f'{preset.DATABASE_NAME}:[ {collection_name.rjust(30)} ]')
    print(f'{section_line(preset.SYMBOL_OVERLINE, preset.LINE_LEN)}')


def get_status(document_id):
    return mongo_stats.find_one({preset.DATABASE_ID: document_id})


def add_status(add_doc):
    try:
        mongo_stats.insert_one({preset.DATABASE_ID: add_doc[preset.DATABASE_ID], 'size': add_doc['size'], 'count': add_doc['count']})
    except DuplicateKeyError as duplicate_key_error:
        print(f'[{duplicate_key_error}]')


def del_status(item_id):
    result = mongo_stats.delete_one({preset.DATABASE_ID: item_id})
    return result.deleted_count == 1


def update_status(collection_id):
    collection_info = get_db_size(collection_id)
    mongo_stats.update_one({preset.DATABASE_ID: collection_id}, {'$set': {'count': collection_info['count'], 'size': collection_info['size']}})


@timed
def delete_collection(collection_name):
    print(f'DELETING [{collection_name}]')
    mongo_database[collection_name].drop()
    del_status(collection_name)


@timed
def export_collection_to_json():
    collection_list = [preset.DATABASE_COLLECTION, preset.DATABASE_COLLECTION_NAMES, preset.DATABASE_COLLECTION_FOLDERS]
    for collection_element in collection_list:
        mongo_collection_item = mongo_database[collection_element]
        with open(f'MongoDB_{collection_element}_Collection_backup.json', preset.WRITE) as file:
            json.dump(list(mongo_collection_item.find({})), file, default=str, indent=4)


@timed
def export_collection_to_json_progress():
    print(f'GENERATING JSON BACKUP... [{preset.DATABASE_COLLECTION}]')
    collection_list = [preset.DATABASE_COLLECTION, preset.DATABASE_COLLECTION_NAMES, preset.DATABASE_COLLECTION_FOLDERS]
    for collection_element in collection_list:
        mongo_collection_item = mongo_database[collection_element]
        with open(f'MongoDB_{collection_element}_Collection_backup.json', preset.WRITE) as file:
            stats_db = get_status(collection_element)
            if not stats_db:
                count = mongo_collection_item.count_documents({})
            else:
                count = stats_db['count']
            with tqdm(total=int(count), bar_format=preset.STATUS_BAR_FORMAT) as tqdm_progress_bar:
                for item in mongo_collection_item.find({}):
                    json.dump(item, file, default=str, indent=4)
                    tqdm_progress_bar.update(1)
    print('DONE.')


if __name__ == preset.__MAIN__:
    parser = argparse.ArgumentParser(description='Create a collection backup')
    parser.add_argument('-n', '--collection_name', type=str, help='New backup name')
    parser.add_argument('-l', '--collection_list', action=preset.STORE_TRUE, help='List collections')
    parser.add_argument('-r', '--refresh_collection', action=preset.STORE_TRUE, help='Refresh collections statuses')
    parser.add_argument('-s', '--collection_size', action=preset.STORE_TRUE, help='List collections with size')
    parser.add_argument('-e', '--collection_export', action=preset.STORE_TRUE, help='Export collection')
    parser.add_argument('-p', '--collection_progress', action=preset.STORE_TRUE, help='Export collection with progress')
    parser.add_argument('-d', '--collection_delete', type=str, help='Delete collection')
    args = parser.parse_args()
    if args.refresh_collection:
        refresh_collections = True
    if args.collection_list:
        list_collections(args.collection_size)
    elif args.collection_name:
        duplicate_collection(args.collection_name)
    elif args.collection_delete:
        delete_collection(args.collection_delete)
    elif args.collection_export:
        export_collection_to_json()
    elif args.collection_progress:
        export_collection_to_json_progress()
    else:
        print('No valid option.')
