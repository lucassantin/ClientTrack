from models.specialty import Specialty
from DAO.dao import DAO

class SpecialtySqliteDAO(DAO):
    """DAO para objetos Specialty, herdando funcionalidades genéricas."""

    def __init__(self):
        super().__init__()

    def create(self, specialty: Specialty) -> Specialty:
        """Salva uma nova especialidade usando o método genérico."""
        data = {
            "id": specialty.id,
            "name": specialty.name,
            "description": specialty.description
        }
        self._insert("specialties", data)
        return specialty

    def _map_row_to_specialty(self, row) -> Specialty:
        """Helper para converter linha do banco (ou dict) em objeto."""
        return Specialty(
            id=row['id'], 
            name=row['name'], 
            description=row['description']
        )

    def find_by_id(self, specialty_id: str) -> Specialty | None:
        """Busca pelo ID usando o método genérico."""
        row = self._fetch_by_id("specialties", specialty_id)
        if row:
            return self._map_row_to_specialty(row)
        return None

    def find_all(self) -> list[Specialty]:
        """Busca todos os registros."""
        rows = self._fetch_all("specialties")
        return [self._map_row_to_specialty(row) for row in rows]

    def update(self, specialty: Specialty) -> Specialty:
        """Atualiza os dados usando o método genérico."""
        data = {
            "name": specialty.name,
            "description": specialty.description
        }
        self._update("specialties", specialty.id, data)
        return specialty

    def delete(self, specialty_id: str) -> bool:
        """Deleta pelo ID usando o método genérico."""
        return self._delete("specialties", specialty_id)