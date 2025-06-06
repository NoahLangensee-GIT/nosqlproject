import time
from pymongo import MongoClient
from Power import Power

MAX_LOGS = 10000

def get_database_collection():
    conn_string = "mongodb://localhost:27017/"
    client = MongoClient(conn_string)
    db = client['power']
    return db.power_logs


def manage_log_limit(collection):
    count = collection.count_documents({})
    if count > MAX_LOGS:
        num_to_delete = count - MAX_LOGS

        print(f"Log-Limit überschritten. {count}/{MAX_LOGS}. Lösche {num_to_delete} älteste(n) Eintrag/Einträge...")

        oldest_docs_cursor = collection.find({}, {"_id": 1}).sort("timestamp", 1).limit(num_to_delete)
        ids_to_delete = [doc["_id"] for doc in oldest_docs_cursor]

        if ids_to_delete:
            collection.delete_many({"_id": {"$in": ids_to_delete}})
            print(f"{len(ids_to_delete)} Einträge gelöscht.")


def start_monitoring():
    try:
        collection = get_database_collection()
        print("✅ Verbindung zur Datenbank erfolgreich. Starte Monitoring...")
    except ValueError as e:
        print(f"❌ Fehler: {e}")
        return

    while True:
        try:
            current_power = Power()
            collection.insert_one(current_power.__dict__)
            print(f"Gespeichert: {current_power}")

            manage_log_limit(collection)

            time.sleep(1)

        except KeyboardInterrupt:
            print("\nMonitoring durch Benutzer beendet.")
            break
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            time.sleep(5)



start_monitoring()