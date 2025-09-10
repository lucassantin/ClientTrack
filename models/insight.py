class Insight:
    def __init__(self, indice: int, recommendation: str):
        self.indice = None
        self.recommendation = None

        def isinstance(indice, int):
            self.indice = indice

        def isinstance(recommendation, str):
            self.recommendation = recommendation

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
