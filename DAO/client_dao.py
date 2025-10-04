import sqlite3
from models.client import Client
from models.user import User
from DAO.user_dao import UserSqliteDAO
from DAO.insight_dao import InsightSqliteDAO

class ClientSqliteDAO:
    """DAO for Client objects, handles both clients and users tables."""

    def __init__(self, db_path: str):
        self.db_path = "clienttrack.db"
        self.user_dao = UserSqliteDAO()
        self.insight_dao = InsightSqliteDAO()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create(self, client: Client) -> Client:
        self.user_dao.create(client)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            insight_id = client.insight.id if client.insight else None
            cursor.execute(
                "INSERT INTO clients (id, birthday, insight_id, accumulated_indice) VALUES (?, ?, ?, ?)",
                (client.id, client.birthDay, insight_id, client.accumulatedIndice)
            )
            conn.commit()
        return client

    def find_by_id(self, client_id: str):
        user = self.user_dao.find_by_id(client_id)
        if not user:
            return None

        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            client_row = cursor.fetchone()
            if client_row:
                insight = self.insight_dao.find_by_id(client_row['insight_id']) if client_row['insight_id'] else None
                user = self.user_dao.find_by_id(client_row['user_id']) if client_row['user_id'] else None
                if user:
                    user = User(user_id=user.user_id, name=user.name, contact=user.contact)

                return Client(
                    id=client_row['id'], name=user.name, contact=user.contact,
                    registered_at=user.registered_at, birthday=client_row['birthday'],
                    accumulated_indice=client_row['accumulated_indice'], insight=insight
                )
        return None

    def find_all(self):
        clients = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.name, u.contact, u.registered_at, c.birthday, c.insight_id, c.accumulated_indice
                FROM users u JOIN clients c ON u.id = c.id
                ORDER BY u.name
            """)
            rows = cursor.fetchall()
            for row in rows:
                insight = self.insight_dao.find_by_id(row['insight_id']) if row['insight_id'] else None
                user = self.user_dao.find_by_id(row['user_id']) if row['user_id'] else None
                if user:
                    user = User(user_id=user.user_id, name=user.name, contact=user.contact)

                clients.append(Client(
                    id=row['id'], name=user.name, contact=user.contact,
                    registered_at=user.registered_at, birthday=row['birthday'],
                    accumulated_indice=row['accumulated_indice'], insight=insight
                ))
        return clients

    def update(self, client: Client):
        self.user_dao.update(client)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            insight_id = client.insight.id if client.insight else None
            cursor.execute(
                "UPDATE clients SET birthday = ?, insight_id = ?, accumulated_indice = ? WHERE id = ?",
                (client.birthDay, insight_id, client.accumulatedIndice, client.id)
            )
            conn.commit()
        return self.find_by_id(client.id)

    def delete(self, client_id: str) -> bool:
        # By using `ON DELETE CASCADE` in the schema, deleting the user
        # will automatically delete the corresponding client record.
        return self.user_dao.delete(client_id)