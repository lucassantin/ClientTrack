from models.payment_type import PaymentType
import datetime
import uuid

class Payment:
    def __init__(self, type: PaymentType, value: float):
        self.__type = None
        self.__value = None
        self.__date_time = datetime.datetime.now()
        self.__id = str(uuid.uuid4())

        if isinstance(type, PaymentType):
            self.__type = type

        if isinstance(value, float):
            self.__value = float(value)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def type(self) -> PaymentType:
        return self.__type
    
    @type.setter
    def type(self, type: PaymentType):
        if isinstance(type, PaymentType):
            self.__type = type
        else:
            raise TypeError("Type must be an instance of TypePayment")
        
    @property
    def value(self) -> float:
        return self.__value
    
    @value.setter
    def value(self, value: float):
        if isinstance(value, (int, float)):
            self.__value = float(value)
        else:
            raise TypeError("Value must be a number")
        
    @property
    def date_time(self) -> datetime.datetime:
        return self.__date_time
