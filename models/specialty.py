import uuid

class Specialty:
    def __init__(self, name:str, description:str, specialty_id:int=None):
        self._specialty_id = None
        self.__name = None
        self.__description = None
        self.__id = str(uuid.uuid4())

        if isinstance(specialty_id, int):
            self._specialty_id = specialty_id

        if isinstance(name, str):
            self.__name = name

        if isinstance(description, str):
            self.__description = description



    @property
    def id(self) -> str:
        return self.__id

    @property
    def specialty_id(self):
        return self._specialty_id
    
    @specialty_id.setter
    def specialty_id(self, specialty_id: int):
        if isinstance(specialty_id,int):
            self._specialty_id = specialty_id


    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self.__name = name
        else:
            raise TypeError("Name must be a string")
        
    @property
    def description(self) -> str:
        return self.__description
    
    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description
        else:
            raise TypeError("Description must be a string")
