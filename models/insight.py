import uuid

class Insight:
    def __init__(self, indice: int, recommendation: str, id: int = None):
        self._id = None
        self._indice = None
        self._recommendation = None
        self.__id = str(uuid.uuid4())
        
        if isinstance(id,int):
            self._id = id

        if isinstance(indice, int):
            self._indice = indice

        if isinstance(recommendation, str):
            self._recommendation = recommendation


    @property
    def id(self) -> str:
        return self.__id

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        if isinstance(id, int):
            self._id = id

    @property
    def indice(self) -> int:
        return self._indice
    
    @indice.setter
    def indice(self, indice: int):
        if isinstance(indice, int):
            self._indice = indice
        else:
            raise TypeError("Indice must be an integer")
        
    @property
    def recommendation(self) -> str:
        return self._recommendation
    
    @recommendation.setter
    def recommendation(self, recommendation: str):
        if isinstance(recommendation, str):
            self._recommendation = recommendation
        else:
            raise TypeError("Recommendation must be a string")
        
