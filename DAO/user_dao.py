from models.user import User
from DAO.dao import DAO

class UserSqliteDAO(DAO):
    """DAO para o modelo base User, herdando funcionalidades genéricas."""

    def __init__(self):
        super().__init__()

    def create(self, user: User) -> User:
        """Cria um novo usuário no banco de dados."""
        data = {
            "id": user.id,
            "name": user.name,
            "contact": user.contact,
            "registered_at": user.registered_at
        }
        self._insert("users", data)
        return user

    def update(self, user: User) -> User:
        """Atualiza os dados de um usuário existente."""
        data = {
            "name": user.name,
            "contact": user.contact
        }
        self._update("users", user.id, data)
        return user

    def delete(self, user_id: str) -> bool:
        """Deleta um usuário pelo ID."""
        return self._delete("users", user_id)

    def find_by_id(self, user_id: str) -> User | None:
        """Busca um usuário pelo ID."""
        row = self._fetch_by_id("users", user_id)
        
        if row:
            return User(**row)
        return None