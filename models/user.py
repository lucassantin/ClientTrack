class User:
    def __init__(self, name: str, contact: str, user_id: int = None):
        self._user_id = None
        self._name = None
        self._contact = None

        if isinstance(user_id, int):
            self._user_id = user_id

        if isinstance(name, str):
            self.name = name

        if isinstance(contact, str):
            self.contact = contact

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id:int):
        if isinstance(user_id, int):
            self._user_id = user_id

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError("Name must be a string")
        
    @property
    def contact(self) -> str:
        return self._contact
    
    @contact.setter
    def contact(self, contact: str):
        if isinstance(contact, str):
            self._contact = contact
        else:
            raise TypeError("Contact must be a string")
