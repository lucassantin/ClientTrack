import uuid

class PaymentType:
    def __init__(self, name: str):
        self.name = None
        self.__id = str(uuid.uuid4())

        if isinstance(name, str):
            self.name = name

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError("Name must be a string")