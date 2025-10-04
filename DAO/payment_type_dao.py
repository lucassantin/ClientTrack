import sqlite3
from models.payment_type import PaymentType

class PaymentTypeSqliteDAO:
    """Concrete DAO for storing PaymentType objects in a SQLite database."""

    def __init__(self):
        self.db_path = "clienttrack.db"

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def create(self, payment_type: PaymentType) -> PaymentType:
        """Saves a new payment type to the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO payment_types (id, name) VALUES (?, ?)",
                (payment_type.id, payment_type.name)
            )
            conn.commit()
        return payment_type

    def find_by_id(self, payment_type_id: str):
        """Finds a payment type by its unique ID."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payment_types WHERE id = ?", (payment_type_id,))
            row = cursor.fetchone()
            if row:
                return PaymentType(id=row['id'], name=row['name'])
        return None

    def find_all(self):
        """Returns a list of all payment types."""
        payment_types = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payment_types")
            rows = cursor.fetchall()
            for row in rows:
                payment_types.append(PaymentType(id=row['id'], name=row['name']))
        return payment_types

    def update(self, payment_type: PaymentType):
        """Updates an existing payment type."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE payment_types SET name = ? WHERE id = ?",
                (payment_type.name, payment_type.id)
            )
            conn.commit()
        return self.find_by_id(payment_type.id)

    def delete(self, payment_type_id: str) -> bool:
        """Deletes a payment type by its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM payment_types WHERE id = ?", (payment_type_id,))
            conn.commit()
            return cursor.rowcount > 0