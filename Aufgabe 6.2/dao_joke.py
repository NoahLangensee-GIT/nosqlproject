from pymongo import MongoClient
from bson.objectid import ObjectId
from joke import Joke


class Dao_joke:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.col = self.client["jokes_db"]["jokes"]

    def insert(self, joke):
        result = self.col.insert_one(joke.__dict__)
        joke._id = result.inserted_id

    def get_category(self, category_name):
        query = {"category": category_name}
        results_cursor = self.col.find(query)
        jokes_list = [Joke(**doc) for doc in results_cursor]
        return jokes_list

    def delete(self, joke_id):
        if not isinstance(joke_id, ObjectId):
            joke_id = ObjectId(joke_id)
        query = {'_id': joke_id}
        self.col.delete_one(query)