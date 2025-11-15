from models.user import User
from models.insight import Insight
import datetime
import uuid

class Client(User):
    def __init__(self, name: str, contact: str, birthDay: str, indice: int, recommendation: str, id:str = None, accumulatedIndice:int = 0, **kwargs):
        super().__init__(name=name, contact=contact, **kwargs)

        self.__id = id if id else str(uuid.uuid4())
        self.__birthDay = None
        self.__accumulatedIndice = None
        self.__register = []
        self.__insight = None

        if isinstance(id, str):
            self.__id = id

        if isinstance(accumulatedIndice, int):
            self.__accumulatedIndice = accumulatedIndice

        if isinstance(birthDay, str):
            try:
                datetime.datetime.strptime(birthDay, "%Y-%m-%d")
                self.__birthDay = birthDay
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if isinstance(indice, int) and isinstance(recommendation, str):
            self.__insight = Insight(indice, recommendation)


    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, id:str):
        if isinstance(id, str):
            self.__id = id

    @property
    def birthDay(self) -> str:
        return self.__birthDay
    
    @birthDay.setter
    def birthDay(self, birthDay: str):
        if isinstance(birthDay, str):
            try:
                datetime.datetime.strptime(birthDay, "%Y-%m-%d")
                self.__birthDay = birthDay
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
        else:
            raise TypeError("BirthDay must be a string in YYYY-MM-DD format")
        
    @property
    def insight(self) -> Insight:
        return self.__insight
    
    @insight.setter
    def insight(self, insight: Insight):
        if isinstance(insight, Insight):
            self.__insight = insight
        else:
            raise TypeError("Insight must be an instance of Insight")
        
    @property
    def register(self) -> list:
        return self.__register
    
    @register.setter
    def register(self, register: 'Appointment'):
        from models.appointment import Appointment 
        if isinstance(register, Appointment):
            self.__register.append(register)
            self.increment_indice() 
        else:
            raise TypeError("Register must be an instance of Appointment")
        
    @property
    def accumulatedIndice(self) -> int:
        return self.__accumulatedIndice
    
    def increment_indice(self, amount: int = 1):
        """Incrementa o índice do cliente."""
        self.__accumulatedIndice += amount

    def can_redeem(self) -> bool:
        """Verifica se o cliente pode resgatar seu insight associado."""
        if not self.__insight:
            return False
        return self.__accumulatedIndice >= self.__insight.indice

    def redeem_insight(self) -> str:
        """Subtrai os pontos do cliente e retorna a recomendação."""
        if self.can_redeem():
            recommendation_text = self.__insight.recommendation
            self.__accumulatedIndice -= self.__insight.indice
            return recommendation_text
        else:
            raise ValueError("Índice acumulado insuficiente para este resgate.")