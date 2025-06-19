from ftplib import print_line

from joke import Joke
from dao_joke import Dao_joke

dao = Dao_joke("mongodb://localhost:27017/")
dao.col.delete_many({})

joke1 = Joke("Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann.", ["Wortspiele"],
             "Autor A")
joke2 = Joke("Was ist grün und rennt durch den Wald? Ein Rudel Gurken.", ["Kurz", "Tiere"], "Autor B")
joke3 = Joke("Treffen sich zwei Jäger. Beide tot.", ["Kurz", "Schwarzer Humor"], "Autor A")
joke4 = Joke("Ich habe einen Witz über Informatiker, aber den verstehen nur die, die ihn schon kennen.",
             ["Informatik", "Wortspiele"], "Autor C")
#insert
dao.insert(joke1)
dao.insert(joke2)
dao.insert(joke3)
dao.insert(joke4)

#get_category
wortspiel_witze = dao.get_category("Wortspiele")
if wortspiel_witze:
    for witz in wortspiel_witze:
        print(f"- {witz}")
else:
    print("Keine Witze in dieser Kategorie gefunden.")

#delete
if wortspiel_witze:
    joke_to_delete = wortspiel_witze[0]
    dao.delete(joke_to_delete._id)
    print_line("After Delete")
    wortspiel_witze = dao.get_category("Wortspiele")
    if wortspiel_witze:
        for witz in wortspiel_witze:
            print(f"- {witz}")
    else:
        print("Keine Witze in dieser Kategorie gefunden.")
else:
    print("Keine Witze zum Löschen gefunden.")
