class User:
    def __init__(self, name: str, contact: str):
        self.name = None
        self.contact = None

        if isinstance(name, str):
            self.name = name

        if isinstance(contact, str):
            self.contact = contact

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
