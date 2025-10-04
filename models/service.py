import uuid
from models.specialty import Specialty

class Service:
    def __init__(self, name: str, description: str, price: float, id: str = None, specialty: Specialty = None):
        self.__name = None
        self.__description = None
        self.__price = None
        self.__specialty = None
        self.__id = id if id else str(uuid.uuid4())

        if isinstance(name, str):
            self.__name = name

        if isinstance(description, str):
            self.__description = description

        if isinstance(price, (int, float)):
            self.__price = float(price)

        if isinstance(id, str):
            self.__id = id

        if isinstance(specialty, Specialty):
            self.__specialty = specialty


    @property
    def specialty(self) -> Specialty:
        return self.__specialty
    
    @specialty.setter
    def specialty(self, specialty: Specialty):
        if isinstance(specialty, Specialty):
            self.__specialty = specialty
        else:
            raise TypeError("Specialty must be a Specialty instance")

    @specialty.setter
    def specialty(self, specialty: Specialty):
        if isinstance(specialty, Specialty):
            self.__specialty = specialty
        else:
            raise TypeError("Specialty must be a Specialty instance")

    @property
    def id(self) -> str:
        return self.__id

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
