import uuid

class PaymentType:
    def __init__(self, name: str, id: str = None):
        self.__name = None
        self.__id = id if id else str(uuid.uuid4())

        if isinstance(name, str):
            self.__name = name
        
        if isinstance(id, str):
            self.__id = id

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