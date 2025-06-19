from pymongo import MongoClient
from room import Room

class Dao_room:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        self.col.insert_one(room.__dict__)

    def read(self):
        doc = self.col.find_one()
        if doc:
            return Room(**doc)
        return None

    def update(self, room):
        query = {'_id': room._id}
        update_data = room.__dict__.copy()
        update_data.pop('_id')
        new_values = {"$set": update_data}
        self.col.update_one(query, new_values)

    def delete(self, room):
        query = {'_id': room._id}
        self.col.delete_one(query)