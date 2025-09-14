from user import User
from models.specialty import Specialty

class Employee(User):
    def __init__(self, name: str, contact: str, specialty: Specialty):
        super().__init__(name, contact)

        self.__specialty = None

        if isinstance(specialty, Specialty):
            self.__specialty = specialty


    @property
    def specialty(self) -> Specialty:
        return self.__specialty

    @specialty.setter
    def specialty(self, specialty: Specialty):
        if isinstance(specialty, Specialty):
            self.__specialty = specialty
        else:
            raise TypeError("Specialty must be an instance of Specialty")
