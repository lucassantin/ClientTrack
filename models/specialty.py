import uuid

class Specialty:
    def __init__(self, name:str, description:str, id:str=None):
        self.__specialty_id = id if id else str(uuid.uuid4())
        self.__name = None
        self.__description = None

        if isinstance(id, str):
            self.__specialty_id = id

        if isinstance(name, str):
            self.__name = name

        if isinstance(description, str):
            self.__description = description



    @property
    def id(self) -> str:
        return self.__specialty_id

    @id.setter
    def id(self, id: str):
        if isinstance(id, str):
            self.__specialty_id = id


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
