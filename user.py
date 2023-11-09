class User:
    _id = -1
    _first_name = "-1"
    _second_name = "-1"

    def __init__(self, id, first_name, second_name):
        self._id = id
        self._first_name = first_name
        self._second_name = second_name

    def getId(self):
        return self._id

    def getFirstName(self):
        return self._first_name

    def getSecondName(self):
        return self._second_name
