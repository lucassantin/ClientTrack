import sqlite3
from models.client import Client
from DAO.user_dao import UserSqliteDAO
from DAO.dao import DAO

class ClientSqliteDAO(DAO):
    """DAO para objetos Client, herdando funcionalidades genéricas."""

    def __init__(self):
        super().__init__()
        self.user_dao = UserSqliteDAO()

    def create(self, client: Client) -> Client:
        """Salva um novo cliente."""
        self.user_dao.create(client)

        data = {
            "id": client.id,
            "birthday": client.birthDay,
            "accumulatedIndice": client.accumulatedIndice,
            "insight_indice": client.insight.indice,
            "insight_recommendation": client.insight.recommendation
        }
        
        self._insert("clients", data)
        return client

    def _map_row_to_client(self, row: sqlite3.Row) -> Client:
        """Helper para converter linha do banco em objeto Client."""
        return Client(
            id=row['id'],
            name=row['name'],
            contact=row['contact'],
            registered_at=row['registered_at'],
            birthDay=row['birthday'],
            accumulatedIndice=row['accumulatedIndice'],
            indice=row['insight_indice'],
            recommendation=row['insight_recommendation']
        )

    def find_all(self) -> list[Client]:
        """Busca todos os clientes (com JOIN em users)."""
        sql = """
            SELECT u.*, c.birthday, c.accumulatedIndice, c.insight_indice, c.insight_recommendation 
            FROM users u 
            JOIN clients c ON u.id = c.id
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
            return [self._map_row_to_client(row) for row in rows]

    def find_by_id(self, client_id: str) -> Client | None:
        """Busca cliente pelo ID (com JOIN em users)."""
        sql = """
            SELECT u.*, c.birthday, c.accumulatedIndice, c.insight_indice, c.insight_recommendation 
            FROM users u 
            JOIN clients c ON u.id = c.id 
            WHERE u.id = ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (client_id,)).fetchone()
            if row:
                return self._map_row_to_client(row)
        return None

    def update(self, client: Client) -> Client:
        """Atualiza cliente."""
        self.user_dao.update(client)
        
        data = {
            "birthday": client.birthDay,
            "accumulatedIndice": client.accumulatedIndice,
            "insight_indice": client.insight.indice,
            "insight_recommendation": client.insight.recommendation
        }
        
        self._update("clients", client.id, data)
        return client

    def update_indice(self, client_id: str, new_indice: int):
        """Atualiza apenas o índice acumulado."""
        data = {"accumulatedIndice": new_indice}
        self._update("clients", client_id, data)

    def delete(self, client_id: str) -> bool:
        """Deleta o cliente (e usuário)."""
        return self.user_dao.delete(client_id)