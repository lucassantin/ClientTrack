import sqlite3
from models.user import User

class UserSqliteDAO:
    """DAO para o modelo base User."""

    def __init__(self):
        self.db_path = "clienttrack.db"

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create(self, user: User) -> User:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (id, name, contact, registered_at) VALUES (?, ?, ?, ?)",
                (user.id, user.name, user.contact, user.registered_at)
            )
            conn.commit()
        return user

    def update(self, user: User) -> User:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, contact = ? WHERE id = ?",
                (user.name, user.contact, user.id)
            )
            conn.commit()
        return user

    def delete(self, user_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            rows_affected = cursor.execute("DELETE FROM users WHERE id = ?", (user_id,)).rowcount
            conn.commit()
            return rows_affected > 0

    def find_by_id(self, user_id: str) -> User | None:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            row = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row:
                return User(**row)
        return None