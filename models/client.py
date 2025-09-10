from user import User
from insight import Insight
from appointment import Appointment
import datetime
class Client(User):
    def __init__(self, name: str, contact: str, birthDay: str, indice: int, recommendation: str):
        super().__init__(name, contact)

        self.birthDay = None
        self.insight = None
        self.register = []
        self.accumulatedIndice = 0

        if isinstance(birthDay, str):
            try:
                datetime.datetime.strptime(birthDay, "%Y-%m-%d")
                self.birthDay = birthDay
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if isinstance(indice, int) and isinstance(recommendation, str):
            self.insight = Insight(indice, recommendation)


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
        return self.accumulatedIndice
    
    def incremmententIndice(self) -> None:
        self.accumulatedIndice += 1

    def isAvailableInsight(self) -> bool:
        return self.accumulatedIndice >= self.insight.indice
    
    def givenInsight(self) -> str:
        if self.isAvailableInsight():
            self.accumulatedIndice -= self.insight.indice
            return self.insight.recommendation
        else:
            return "Not enough accumulated indice to receive insight."