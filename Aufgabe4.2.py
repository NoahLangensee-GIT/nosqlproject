import os

from pymongo import MongoClient

connection_string = os.environ.get('DB_CONNECTION')

if connection_string:

    client = MongoClient(connection_string)
    print(client.server_info())
else:
    print("Fehler: Die Umgebungsvariable 'DB_CONNECTION' wurde nicht gefunden.")