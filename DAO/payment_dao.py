import sqlite3
from models.payment import Payment
from models.payment_type import PaymentType
from DAO.payment_type_dao import PaymentTypeSqliteDAO
from DAO.dao import DAO
class PaymentSqliteDAO(DAO):
    """DAO para objetos Payment, lida com a tabela payments."""

    def __init__(self):
        super().__init__()
        self.payment_type_dao = PaymentTypeSqliteDAO()

    def _get_connection(self) -> sqlite3.Connection:
        """Estabelece uma conexão com o banco de dados."""
        return sqlite3.connect(self._db_path)

    def create(self, payment: Payment) -> Payment:
        """Salva um novo pagamento no banco de dados."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO payments (id, value, date_time, typePayment_id) VALUES (?, ?, ?, ?)",
                (payment.id, payment.value, payment.date_time, payment.payment_type.id)
            )
            conn.commit()
        return payment

    def _map_row_to_payment(self, row: sqlite3.Row) -> Payment | None:
        """Cria um objeto Payment a partir de uma linha do banco."""
        payment_type = self.payment_type_dao.find_by_id(row['typePayment_id'])
        if not payment_type:
            return None

        return Payment( 
            id=row['id'],
            value=row['value'],
            date_time=row['date_time'],
            payment_type=payment_type
        )

    def find_by_id(self, payment_id: str) -> Payment | None:
        """Encontra um pagamento pelo seu ID único."""
        sql = "SELECT * FROM payments WHERE id = ?"
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (payment_id,)).fetchone()
            if row:
                return self._map_row_to_payment(row)
        return None

    def find_all(self) -> list[Payment]:
        """Retorna uma lista de todos os pagamentos."""
        payments = []
        sql = "SELECT * FROM payments ORDER BY date_time DESC"
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
            for row in rows:
                payment_obj = self._map_row_to_payment(row)
                if payment_obj:
                    payments.append(payment_obj)
        return payments

    def update(self, payment: Payment) -> Payment:
        """Atualiza um pagamento existente."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE payments SET value = ?, date_time = ?, typePayment_id = ? WHERE id = ?",
                (payment.value, payment.date_time, payment.payment_type.id, payment.id)
            )
            conn.commit()
        return payment 

    def delete(self, payment_id: str) -> bool:
        """Deleta um pagamento pelo seu ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            rows_affected = cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,)).rowcount
            conn.commit()
            return rows_affected > 0