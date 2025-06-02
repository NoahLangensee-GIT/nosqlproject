from pymongo import MongoClient
import bson

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)


def run_explorer():
	dblist = client.list_database_names()
	print("\nDatabases")
	if not dblist:
		print("\nNo Database")
		press_any_key()
		return
	while True:
		for db in dblist:
			print(" - " + db)
		dbname = input("\nSelect Database: ")
		if dbname in dblist:
			selected_db = client[dbname]
			collist = selected_db.list_collection_names()
			print("\n" + selected_db.name)
			print("\nCollections")
			if not collist:
				print("\nNo Collection")
				press_any_key()
				return
			while True:
				for col in collist:
					print(" - " + col)
				colname = input("\nSelect Collection: ")
				if colname in collist:
					selected_col = selected_db[colname]
					doclist = list(selected_col.find())
					print("\n" + selected_db.name + "." + selected_col.name)
					print("\nDocuments")
					if not doclist:
						print("\nNo Document")
						press_any_key()
						return
					while True:
						doc_ids = []
						for doc in doclist:
							doc_ids.append(str(doc["_id"]))
							print(" - " + str(doc['_id']))
						doc_id = input("\nSelect Document: ")
						for doc in doclist:
							if str(doc["_id"]) == doc_id:
								print("\n" + selected_db.name + "." + selected_col.name + "." + doc_id +"\n")
								doc_id = bson.ObjectId(doc_id)
								query = {"_id": doc_id}
								module = selected_col.find_one(query)
								for key, value in module.items():
									if key == "_id":
										continue
									print(f"{key}: {value}")
								press_any_key()
								return

						print("\nDocument does not exist")
				else:
					print("\nCollection does not exist.")
		else:
			print("\nDatabase does not exist.")

def press_any_key():
	input("\nPress any button to return")
	run_explorer()

run_explorer()