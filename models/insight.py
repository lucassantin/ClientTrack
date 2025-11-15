import uuid

class Insight:
    def __init__(self, indice: int, recommendation: str, id: int = None):
        self.__id = None
        self.__indice = None
        self.__recommendation = None
        self.__id = str(uuid.uuid4())
        
        if isinstance(id,int):
            self.__id = id

        if isinstance(indice, int):
            self.__indice = indice

        if isinstance(recommendation, str):
            self.__recommendation = recommendation


    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: int):
        if isinstance(id, int):
            self.__id = id

    @property
    def indice(self) -> int:
        return self.__indice
    
    @indice.setter
    def indice(self, indice: int):
        if isinstance(indice, int):
            self.__indice = indice
        else:
            raise TypeError("Indice must be an integer")
        
    @property
    def recommendation(self) -> str:
        return self.__recommendation
    
    @recommendation.setter
    def recommendation(self, recommendation: str):
        if isinstance(recommendation, str):
            self.__recommendation = recommendation
        else:
            raise TypeError("Recommendation must be a string")
        
