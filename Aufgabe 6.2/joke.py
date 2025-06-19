class Joke:
    def __init__(self, text, category, author, _id = None):
        if _id is not None:
            self._id = _id
        self.text = text
        self.category = category
        self.author = author

    def __str__(self):
        return f'"{self.text}" (Kategorie: {", ".join(self.category)}) - von {self.author}'