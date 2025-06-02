from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.restaurants
restaurants_collection = db.restaurants


def print_restaurant_details(restaurant):
    print(f"  Name: {restaurant.get('name')}")
    print(f"  Küche: {restaurant.get('cuisine')}")
    print(f"  Bezirk: {restaurant.get('borough')}")
    print(
        f"  Adresse: {restaurant['address'].get('street', '')}, {restaurant['address'].get('zipcode', '')} {restaurant['address'].get('building', '')}")
    avg_score = sum(grade.get('score') for grade in restaurant['grades']) / len(restaurant['grades'])
    print(f"  Durchschnittliche Bewertung: {avg_score:.2f}")
    print(f"  ID: {restaurant.get('restaurant_id')}")
    print("-" * 30)


def get_unique_boroughs():
    print("Aufgabe 1: Einzigartige Stadtbezirke")
    distinct_boroughs = restaurants_collection.distinct("borough")
    if distinct_boroughs:
        print("Folgende Stadtbezirke sind vorhanden:")
        for borough in distinct_boroughs:
            print(f"- {borough}")
    else:
        print("Keine Stadtbezirke gefunden.")

    print("\n" + "-" * 50 + "\n")


def get_top_3_restaurants_by_average_score():
    print("Aufgabe 2: Top 3 Restaurants nach Durchschnitts-Rating")

    pipeline = [
        {
            "$unwind": "$grades"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "borough": {"$first": "$borough"},
                "cuisine": {"$first": "$cuisine"},
                "address": {"$first": "$address"},
                "original_grades": {"$push": "$grades"},
                "averageScore": {"$avg": "$grades.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        },
        {
            "$limit": 3
        }
    ]
    top_restaurants = list(restaurants_collection.aggregate(pipeline))

    if top_restaurants:
        print("Die Top 3 Restaurants mit dem höchsten Durchschnitts-Rating sind:")
        for i, r in enumerate(top_restaurants):
            print(f"\n{i + 1}. Name: {r['name']}")
            print(f"   Bezirk: {r['borough']}")
            print(f"   Küche: {r['cuisine']}")
            print(f"   Durchschnitts-Score: {r['averageScore']:.2f}")
            print(f"   ID: {r['_id']}")
    else:
        print("Keine Restaurants für die Top-Rating-Liste gefunden.")
    print("\n" + "-" * 50 + "\n")


def find_restaurant_nearest_to_le_perigord():
    print("Aufgabe 3: Restaurant am nächsten zu 'Le Perigord'")
    le_perigord = restaurants_collection.find_one({"name": "Le Perigord"})
    le_perigord_coords = le_perigord["address"]["coord"]
    print(f"Koordinaten von 'Le Perigord': {le_perigord_coords}")

    nearest_restaurant_cursor = restaurants_collection.find({
        "address.coord": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": le_perigord_coords
                },
            }
        },
        "_id": {"$ne": le_perigord["_id"]}
    }).limit(1)

    if nearest_restaurant_cursor:
        print("\nDas nächstgelegene Restaurant zu 'Le Perigord' ist:")
        print_restaurant_details(nearest_restaurant_cursor[0])
    else:
        print("Kein anderes Restaurant in der Nähe von 'Le Perigord' gefunden.")
    print("\n" + "=" * 50 + "\n")


def search_restaurants_app():
    selected_restaurant_id_for_grading = None
    print("Aufgabe 4 & 5: Restaurant-Such- und Bewertungsapplikation")

    while True:
        print("\nRestaurant-Suche:")
        search_name = input("Name des Restaurants (leer lassen für keine Suche nach Name): ")
        search_cuisine = input("Küche (leer lassen für keine Suche nach Küche): ")

        query = {}
        if search_name:
            query["name"] = {"$regex": search_name, "$options": "i"}
        if search_cuisine:
            query["cuisine"] = {"$regex": search_cuisine, "$options": "i"}

        if not query:
            user_cmd = input("Bitte geben Sie mindestens ein Suchkriterium an oder 'exit' zum Beenden: ")
            if user_cmd == 'exit':
                break
            continue

        found_restaurants = list(restaurants_collection.find(query))

        if not found_restaurants:
            print("Keine Restaurants für Ihre Suchkriterien gefunden.")
            selected_restaurant_id_for_grading = None
        elif len(found_restaurants) == 1:
            print("\nEin Restaurant gefunden:")
            print_restaurant_details(found_restaurants[0])
            selected_restaurant_id_for_grading = found_restaurants[0]['_id']
        else:
            print(f"\n{len(found_restaurants)} Restaurants gefunden. Bitte wählen Sie eines aus:")
            for i, r in enumerate(found_restaurants):
                print(f"{i + 1}. {r.get('name')} ({r.get('cuisine')}) - ID: {r.get('_id')}")

            while True:
                try:
                    choice = input(f"Wählen Sie eine Nummer (1-{len(found_restaurants)}) oder '0' für keine Auswahl: ")
                    choice_int = int(choice)
                    if choice_int == 0:
                        selected_restaurant_id_for_grading = None
                        print("Kein Restaurant für Bewertung ausgewählt.")
                        break
                    if 1 <= choice_int <= len(found_restaurants):
                        selected_restaurant_id_for_grading = found_restaurants[choice_int - 1]['_id']
                        print("\nAusgewähltes Restaurant:")
                        print_restaurant_details(found_restaurants[choice_int - 1])
                        break
                    else:
                        print("Ungültige Auswahl.")
                except ValueError:
                    print("Bitte geben Sie eine Zahl ein.")

        if selected_restaurant_id_for_grading:
            add_grade_prompt = input("Möchten Sie diesem Restaurant eine Bewertung hinzufügen? (j/n): ")
            if add_grade_prompt == 'j':
                while True:
                    grade_input = input("Bewertung (z.B. A, B, C): ")
                    if not grade_input:
                        print("Bewertung darf nicht leer sein.")
                        continue
                    try:
                        score_input_str = input("Score (Zahl): ")
                        score_input = int(score_input_str)
                        break
                    except ValueError:
                        print("Ungültiger Score. Bitte geben Sie eine ganze Zahl ein.")

                new_grade = {
                    "date": datetime.now(),
                    "grade": grade_input,
                    "score": score_input
                }

                update_result = restaurants_collection.update_one(
                    {"_id": selected_restaurant_id_for_grading},
                    {"$push": {"grades": new_grade}}
                )
                if update_result.modified_count > 0:
                    print("Bewertung erfolgreich hinzugefügt!")
                    updated_restaurant = restaurants_collection.find_one(
                        {"_id": selected_restaurant_id_for_grading})
                    print("\nAktualisierte Restaurantdetails:")
                    print_restaurant_details(updated_restaurant)

        continue_app = input("\nWeitere Suche durchführen oder bewerten? (j/n zum Beenden): ")
        if continue_app != 'j':
            break


print("\nApplikation beendet.")
print("\n" + "=" * 50 + "\n")

get_unique_boroughs()

get_top_3_restaurants_by_average_score()

find_restaurant_nearest_to_le_perigord()

search_restaurants_app()

client.close()
print("MongoDB Verbindung geschlossen.")
