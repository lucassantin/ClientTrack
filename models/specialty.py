class Specialty:
    def __init__(self, name, description):
        self.__name = None
        self.__description = None

        if isinstance(name, str):
            self.__name = name

        if isinstance(description, str):
            self.__description = description


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
