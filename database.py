import preset
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

mongo_client = MongoClient(preset.DATABASE_URL)
mongo_database = mongo_client[preset.DATABASE_NAME]
mongo_collection = mongo_database[preset.DATABASE_COLLECTION]
mongo_collection_folders = mongo_database[preset.DATABASE_COLLECTION_FOLDERS]
mongo_collection_names = mongo_database[preset.DATABASE_COLLECTION_NAMES]


def insert_url(item):
    try:
        mongo_collection.insert_one(item)
    except DuplicateKeyError:
        mongo_collection.update_one({preset.DATABASE_ID: item[preset.DATABASE_ID]}, {preset.SET: {preset.FOLDER_INFO_NAME_PROPOSAL: item[preset.FOLDER_INFO_NAME_PROPOSAL]}}, upsert=True)


def insert_name(item):
    try:
        mongo_collection_names.insert_one(item)
    except DuplicateKeyError:
        mongo_collection_names.update_one({preset.DATABASE_ID: item[preset.DATABASE_ID]}, {preset.SET: {preset.URL_NAME: item[preset.URL_NAME]}}, upsert=True)


def get_name(item):
    return mongo_collection_names.find_one({preset.DATABASE_ID: item})


def insert_item(item):
    try:
        mongo_collection_folders.insert_one(item)
    except DuplicateKeyError:
        mongo_collection_folders.update_one({preset.DATABASE_ID: item[preset.DATABASE_ID]}, {preset.SET: {preset.FOLDER_INFO_NAME_PROPOSAL: item[preset.FOLDER_INFO_NAME_PROPOSAL]}}, upsert=True)


def get_item(item):
    return mongo_collection_folders.find_one({preset.DATABASE_ID: item})
