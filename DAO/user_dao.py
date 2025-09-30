import sqlite3
from models.user import User
from models.client import Client

class UserSqliteDAO:
    """DAO for the base User model."""

    def __init__(self):
        self.db_path = "clienttrack.db"

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create(self, user):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (id, name, contact, registered_at) VALUES (?, ?, ?, ?)",
                (user.id, user.name, user.contact, user.registered_at)
            )
            conn.commit()
        return user

    def find_by_id(self, user_id: str):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
                    id=row['id'],
                    name=row['name'],
                    contact=row['contact'],
                    registered_at=row['registered_at']
                )
        return None

    def update(self, user):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, contact = ? WHERE id = ?",
                (user.name, user.contact, user.user_id)
            )
            conn.commit()
        return self.find_by_id(user.user_id)

    def delete(self, user_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0