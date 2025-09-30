import uuid

class Service:
    def __init__(self, name: str, description: str, price: float):
        self.__name = None
        self.__description = None
        self.__price = None
        self.__id = str(uuid.uuid4())

        if isinstance(name, str):
            self.__name = name

        if isinstance(description, str):
            self.__description = description

        if isinstance(price, (int, float)):
            self.__price = float(price)


    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self.__name = name
        else:
            raise TypeError("Name must be a string")

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description
        else:
            raise TypeError("Description must be a string")

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, price: float):
        if isinstance(price, (int, float)):
            self.__price = float(price)
        else:
            raise TypeError("Price must be a number")
