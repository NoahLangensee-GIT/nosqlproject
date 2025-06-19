class Room:
    def __init__(self, name, seats, is_reservable, _id = None):
        if _id is not None:
            self._id = _id
        self.name = name
        self.seats = seats
        self.is_reservable = is_reservable

    def __str__(self):
        return f"{self.name} with {self.seats} seats is reservable: {self.is_reservable}"