from models.payment_type import PaymentType
import datetime
import uuid

class Payment:
    def __init__(self, payment_type: PaymentType, value: float, date_time:str=None, id:str=None):
        self.__payment_type = None
        self.__value = None
        self.__date_time = date_time if date_time else datetime.datetime.now()
        self.__id = id if id else str(uuid.uuid4())

        if isinstance(payment_type, PaymentType):
            self.__payment_type = payment_type

        if isinstance(value, float):
            self.__value = float(value)
 
    @property
    def id(self) -> str:
        return self.__id

    @property
    def payment_type(self) -> PaymentType:
        return self.__payment_type
    
    @payment_type.setter
    def payment_type(self, payment_type: PaymentType):
        if isinstance(payment_type, PaymentType):
            self.__payment_type = payment_type
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
