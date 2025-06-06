import time
import matplotlib.pyplot as plt
from pymongo import MongoClient


def get_database_collection():
    conn_string = "mongodb://localhost:27017/"
    client = MongoClient(conn_string)
    db = client['power']
    return db.power_logs


def plot_data():
    while True:
        try:
            print("Lade Daten und erstelle den Graphen...")
            try:
                collection = get_database_collection()
                logs = list(collection.find({}).sort("timestamp", 1))
            except ValueError as e:
                print(f"❌ Fehler: {e}")
                return

            if not logs:
                print("Keine Daten zum Anzeigen in der Datenbank gefunden.")
                return

            timestamps = [log['timestamp'] for log in logs]
            cpu_usage = [log['cpu_percent'] for log in logs]
            ram_usage_percent = [(log['ram_used'] / log['ram_total']) * 100 for log in logs]

            fig, ax = plt.subplots(figsize=(15, 7))

            ax.plot(timestamps, cpu_usage, label='CPU Auslastung (%)', color='blue')
            ax.plot(timestamps, ram_usage_percent, label='RAM Auslastung (%)', color='green')

            ax.set_title('Systemauslastung über Zeit')
            ax.set_xlabel('Zeitstempel')
            ax.set_ylabel('Auslastung in %')
            ax.legend()
            ax.grid(True)

            fig.autofmt_xdate()

            plt.tight_layout()
            plt.show()
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nMonitoring durch Benutzer beendet.")
            break



plot_data()