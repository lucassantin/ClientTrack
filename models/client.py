from models.user import User
from models.insight import Insight
from models.appointment import Appointment
import datetime
import uuid

class Client(User):
    def __init__(self, name: str, contact: str, birthDay: str, indice: int, recommendation: str, user_id:int =None, id:int = None):
        super().__init__(name, contact, user_id=user_id)

        self._id = None
        self._birthDay = None
        self._insight = None
        self._register = []
        self._accumulatedIndice = 0
        self.__id = str(uuid.uuid4())

        if isinstance(id, int):
            self._id = id

        if isinstance(birthDay, str):
            try:
                datetime.datetime.strptime(birthDay, "%Y-%m-%d")
                self._birthDay = birthDay
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if isinstance(indice, int) and isinstance(recommendation, str):
            self._insight = Insight(indice, recommendation)


    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id:int):
        if isinstance(id, int):
            self._id = id

    @property
    def birthDay(self) -> str:
        return self._birthDay
    
    @birthDay.setter
    def birthDay(self, birthDay: str):
        if isinstance(birthDay, str):
            try:
                datetime.datetime.strptime(birthDay, "%Y-%m-%d")
                self._birthDay = birthDay
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
        else:
            raise TypeError("BirthDay must be a string in YYYY-MM-DD format")
        
    @property
    def insight(self) -> Insight:
        return self._insight
    
    @insight.setter
    def insight(self, insight: Insight):
        if isinstance(insight, Insight):
            self._insight = insight
        else:
            raise TypeError("Insight must be an instance of Insight")
        
    @property
    def register(self) -> list:
        return self._register
    
    @register.setter
    def register(self, register: Appointment):
        if isinstance(register, Appointment):
            self._register.append(register)
            self.incremmententIndice()
        else:
            raise TypeError("Register must be an instance of Appointment")
        
    @property
    def accumulatedIndice(self) -> int:
        return self._accumulatedIndice
    
    def incremmententIndice(self) -> None:
        self._accumulatedIndice += 1

    def isAvailableInsight(self) -> bool:
        return self._accumulatedIndice >= self.insight.indice
    
    def givenInsight(self) -> str:
        if self.isAvailableInsight():
            self._accumulatedIndice -= self.insight.indice
            return self.insight.recommendation
        else:
            return "Not enough accumulated indice to receive insight."