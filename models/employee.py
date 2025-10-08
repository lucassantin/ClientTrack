from models.user import User
from models.specialty import Specialty
import uuid


class Employee(User):
    def __init__(self, name: str, contact: str, specialty: Specialty, id: str = None, **kwargs):
        super().__init__(name=name, contact=contact, **kwargs)

        self.__specialty = None
        self.__id = id if id else str(uuid.uuid4())

        if isinstance(id, str):
            self.__id = id

        if isinstance(specialty, Specialty):
            self.__specialty = specialty


    @property
    def id(self) -> str:
        return self.__id

    @property
    def specialty(self) -> Specialty:
        return self.__specialty

    @specialty.setter
    def specialty(self, specialty: Specialty):
        if isinstance(specialty, Specialty):
            self.__specialty = specialty
        else:
            raise TypeError("Specialty must be an instance of Specialty")
