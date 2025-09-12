from user import User
from especiality import Especiality

class Employee(User):
    def __init__(self, name: str, contact: str, especiality: Especiality):
        super().__init__(name, contact)

        self.__especiality = None

        if isinstance(especiality, Especiality):
            self.__especiality = especiality


    @property
    def especiality(self) -> Especiality:
        return self.__especiality

    @especiality.setter
    def especiality(self, especiality: Especiality):
        if isinstance(especiality, Especiality):
            self.__especiality = especiality
        else:
            raise TypeError("Especiality must be an instance of Especiality")
