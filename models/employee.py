from models.user import User
from models.specialty import Specialty
import uuid


class Employee(User):
    def __init__(self, name: str, contact: str, specialty: Specialty, id: str = str(uuid.uuid4()), user_id: str = None):
        super().__init__(name=name, contact=contact, user_id=user_id)

        self.__specialty = None
        self.__id = None

        if isinstance(id, str):
            self.__id = id

        if isinstance(specialty, Specialty):
            self.__specialty = specialty


    @property
    def id(self) -> str:
        return self.__id

    @property
    def employee_id(self):
        return self._employee_id
    
    @employee_id.setter
    def employee_id(self, employee_id: int):
        if isinstance(employee_id, int):
            self._employee_id = employee_id

    @property
    def specialty(self) -> Specialty:
        return self.__specialty

    @specialty.setter
    def specialty(self, specialty: Specialty):
        if isinstance(specialty, Specialty):
            self.__specialty = specialty
        else:
            raise TypeError("Specialty must be an instance of Specialty")
