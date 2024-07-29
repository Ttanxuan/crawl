# encoding  = utf-8
import pymongo


class MyMongoDB():
    def __init__(self):
        super(MyMongoDB, self).__init__()
        self.insert_one = None
        self.db = None
        self.coll = None
        self.find_chapter = None
        self.findall = None
        self.insert = None
        self.my_client = pymongo.MongoClient('mongodb://localhost:27017/')

    def db_insert(self, client_name: str, title: str, insert_dicts):
        self.db = self.my_client[client_name]
        self.coll = self.db[title]
        if isinstance(insert_dicts, list) and len(insert_dicts) > 0:
            self.insert = self.coll.insert_many(insert_dicts)
        elif isinstance(insert_dicts, dict):
            self.insert_one = self.coll.insert_one(insert_dicts)
        else:
            raise TypeError("insert_dicts should be either a non-empty list of dictionaries or a single dictionary")

    def db_find(self, client_name: str, title: str, chapter):
        self.db = self.my_client[client_name]
        self.coll = self.db[title]
        self.findall = self.coll.find()

    def db_find_one(self, client_name: str, title: str, chapter):
        self.db = self.my_client[client_name]
        self.coll = self.db[title]
        self.find_chapter = self.coll.find({"chapter": chapter})
