import sqlite3
from models.payment import Payment
from models.payment_type import PaymentType
from DAO.payment_type_dao import PaymentTypeSqliteDAO

class PaymentSqliteDAO:
    """Concrete DAO for storing Payment objects in a SQLite database."""

    def __init__(self):
        self.db_path = "clienttrack.db"
        self.payment_type_dao = PaymentTypeSqliteDAO()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def create(self, payment: Payment) -> Payment:
        """Saves a new payment to the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO payments (id, value, date_time, typePayment_id) VALUES (?, ?, ?, ?)",
                (payment.id, payment.value, payment.date_time, payment.type.id)
            )
            conn.commit()
        return payment

    def find_by_id(self, payment_id: str):
        """Finds a payment by its unique ID."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
            row = cursor.fetchone()
            if row:
                payment_type = self.payment_type_dao.find_by_id(row['payment_type_id'])
                if payment_type:
                    return Payment(
                        id=row['id'],
                        value=row['value'],
                        date_time=row['date_time'],
                        payment_type=payment_type
                    )
        return None

    def find_all(self):
        """Returns a list of all payments."""
        payments = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payments ORDER BY date_time DESC")
            rows = cursor.fetchall()
            for row in rows:
                payment_type = self.payment_type_dao.find_by_id(row['payment_type_id'])
                if payment_type:
                    payments.append(Payment(
                        id=row['id'],
                        value=row['value'],
                        date_time=row['date_time'],
                        payment_type=payment_type
                    ))
        return payments

    def update(self, payment: Payment):
        """Updates an existing payment."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE payments SET value = ?, date_time = ?, payment_type_id = ? WHERE id = ?",
                (payment.value, payment.date_time, payment.payment_type.id, payment.id)
            )
            conn.commit()
        return self.find_by_id(payment.id)

    def delete(self, payment_id: str) -> bool:
        """Deletes a payment by its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
            conn.commit()
            return cursor.rowcount > 0