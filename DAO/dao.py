class DAO:
    def __init__(self):
        self.__data = {}
        self._db_path = "clienttrack.db"

    def create(self, key, value):
        if key in self.__data:
            raise KeyError(f"Key {key} already exists.")
        self.__data[key] = value

    def read(self, key):
        if key not in self.__data:
            raise KeyError(f"Key {key} not found.")
        return self.__data[key]

    def update(self, key, value):
        if key not in self.__data:
            raise KeyError(f"Key {key} not found.")
        self.__data[key] = value

    def delete(self, key):
        if key not in self.__data:
            raise KeyError(f"Key {key} not found.")
        del self.__data[key]

    def list_all(self):
        return self.__data.items()