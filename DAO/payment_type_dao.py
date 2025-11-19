from models.payment_type import PaymentType
from DAO.dao import DAO

class PaymentTypeSqliteDAO(DAO):
    """Concrete DAO for storing PaymentType objects, herdando funcionalidades genéricas."""

    def __init__(self):
        super().__init__()

    def create(self, payment_type: PaymentType) -> PaymentType:
        """Salva um novo tipo de pagamento usando o método genérico."""
        data = {
            "id": payment_type.id,
            "name": payment_type.name
        }
        self._insert("payment_types", data)
        return payment_type

    def find_by_id(self, payment_type_id: str) -> PaymentType | None:
        """Busca pelo ID usando o método genérico."""
        row = self._fetch_by_id("payment_types", payment_type_id)
        
        if row:
            return PaymentType(id=row['id'], name=row['name'])
        return None

    def find_all(self) -> list[PaymentType]:
        """Busca todos os registros."""
        rows = self._fetch_all("payment_types")
        
        return [PaymentType(id=row['id'], name=row['name']) for row in rows]

    def update(self, payment_type: PaymentType) -> PaymentType:
        """Atualiza os dados usando o método genérico."""
        data = {
            "name": payment_type.name
        }
        self._update("payment_types", payment_type.id, data)
        
        return payment_type

    def delete(self, payment_type_id: str) -> bool:
        """Deleta pelo ID usando o método genérico."""
        return self._delete("payment_types", payment_type_id)