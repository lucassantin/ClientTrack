from models.user import User
from models.specialty import Specialty
import uuid


class Employee(User):
    def __init__(self, name: str, contact: str, specialty: Specialty | None = None, id: str = None, **kwargs):
        super().__init__(name=name, contact=contact, **kwargs)

        self.__specialty = specialty
        self.__id = id if id else str(uuid.uuid4())

        if isinstance(id, str):
            self.__id = id


    @property
    def id(self) -> str:
        return self.__id

    @property
    def specialty(self) -> Specialty | None:
        return self.__specialty

    @specialty.setter
    def specialty(self, specialty: Specialty | None):
        if isinstance(specialty, Specialty) or specialty is None:
            self.__specialty = specialty
        else:
            raise TypeError("Specialty must be an instance of Specialty or None")