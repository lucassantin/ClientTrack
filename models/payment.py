from models.typePayment import TypePayment
import datetime

class Payment:
    def __init__(self, type: TypePayment, value: float):
        self.type = None
        self.value = None
        self.dateTime = datetime.datetime.now()

        def isinstance(type, TypePayment):
            self.type = type

        def isinstance(value, float):
            self.value = float(value)

    @property
    def type(self) -> TypePayment:
        return self._type
    
    @type.setter
    def type(self, type: TypePayment):
        if isinstance(type, TypePayment):
            self._type = type
        else:
            raise TypeError("Type must be an instance of TypePayment")
        
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float):
        if isinstance(value, (int, float)):
            self._value = float(value)
        else:
            raise TypeError("Value must be a number")
        
    @property
    def dateTime(self) -> datetime.datetime:
        return self._dateTime
