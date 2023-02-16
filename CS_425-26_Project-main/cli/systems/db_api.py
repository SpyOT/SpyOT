from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoAPI:
    def __init__(self, db_name="default_db"):
        is_prod = os.getenv('DB_ENV')
        CONNECTION_STRING = "temp" if not is_prod else "mongodb://localhost:27017"
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[db_name]
        self.collections = {}

    def create_collection(self, collection_name):
        self.collections[collection_name] = self.db[collection_name]

    def insert_into_collection(self, collection_name, entries):
        self.dest_collection = self.collections[collection_name]
        self.dest_collection.insert_many([entries])

    def get_collection_data(self):
        collection_names = self.get_collection_names()
        collection = self.db[collection_names[0]]
        return collection.find()

    def get_collection_names(self):
        return self.db.list_collection_names()

    def is_db_setup(self):
        return len(self.get_collection_names()) != 0