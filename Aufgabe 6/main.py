from room import Room
from dao_room import Dao_room

dao_room = Dao_room("mongodb://localhost:27017/")

# Create
room_create = Room("Pilatus", 12, True)
dao_room.create(room_create)

# Read
room_read = dao_room.read()
print(room_read)

# Update
room_read.seats = 20  # Ändere die Anzahl der Sitze
dao_room.update(room_read)
room_read = dao_room.read()
print(room_read)

# Delete
dao_room.delete(room_read)
room_read = dao_room.read()
print(room_read)