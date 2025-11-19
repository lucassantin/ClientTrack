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


    def create(self, payment: Payment) -> Payment:
        """Salva um novo pagamento usando o método genérico _insert."""
        
        data = {
            "id": payment.id,
            "value": payment.value,
            "date_time": payment.date_time,
            "typePayment_id": payment.payment_type.id
        }
        
        self._insert("payments", data)
        
        return payment

    def _map_row_to_payment(self, row) -> Payment | None:
        """
        Converte uma linha do banco (ou dict do cache) em um objeto Payment.
        """
        
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
        """Busca usando o método genérico _fetch_by_id."""
        row = self._fetch_by_id("payments", payment_id)
        
        if row:
            return self._map_row_to_payment(row)
        return None

    def find_all(self) -> list[Payment]:
        """Busca todos usando _fetch_all e aplica ordenação via Python."""
        rows = self._fetch_all("payments")
        payments = []
        
        for row in rows:
            payment_obj = self._map_row_to_payment(row)
            if payment_obj:
                payments.append(payment_obj)
        
        payments.sort(key=lambda x: x.date_time, reverse=True)
        
        return payments

    def update(self, payment: Payment) -> Payment:
        """Atualiza usando o método genérico _update."""
        
        data = {
            "value": payment.value,
            "date_time": payment.date_time,
            "typePayment_id": payment.payment_type.id
        }
        
        self._update("payments", payment.id, data)
        
        return payment

    def delete(self, payment_id: str) -> bool:
        """Deleta usando o método genérico _delete."""
        return self._delete("payments", payment_id)