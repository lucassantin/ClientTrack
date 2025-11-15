from abc import ABC
import uuid
import datetime
from abc import ABC

class User(ABC):
    def __init__(self, name: str, contact: str, id: str = None, registered_at: str = None):
        self.__name = None
        self.__contact = None
        self.__registered_at = registered_at if registered_at else datetime.datetime.now().isoformat()
        self.__id = id if id else str(uuid.uuid4())

        if isinstance(id, str):
            self.__id = id

        if isinstance(name, str):
            self.name = name

        if isinstance(contact, str):
            self.contact = contact
        
        if isinstance(registered_at, str):
            self.__registered_at = registered_at

    @property
    def registered_at(self):
        return self.__registered_at
    
    @registered_at.setter
    def registered_at(self, registered_at: str):
        if isinstance(registered_at, str):
            self.__registered_at = registered_at
        else:
            raise TypeError("registered_at must be a string")

    @property
    def id(self) -> str:
        return self.__id

    
    
    @id.setter
    def id(self, id:str):
        if isinstance(id, str):
            self.__id = id

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
    def contact(self) -> str:
        return self.__contact
    
    @contact.setter
    def contact(self, contact: str):
        if isinstance(contact, str):
            self.__contact = contact
        else:
            raise TypeError("Contact must be a string")
