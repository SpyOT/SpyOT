from pymongo import MongoClient

class MongoAPI:
    def __init__(self, db_name="default_db"):
        CONNECTION_STRING = "mongodb://localhost:27017"
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[db_name]
        self.collections = {}

    def create_collection(self, collection_name):
        self.collections[collection_name] = self.db[collection_name]

    def insert_into_collection(self, collection_name, entries):
        self.dest_collection = self.collections[collection_name]
        self.dest_collection.insert_many([entries])

    def is_db_setup(self):
        return len(self.db.list_collection_names()) != 0