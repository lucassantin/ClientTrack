from models.insight import Insight
from DAO.dao import DAO

class InsightSqliteDAO(DAO):
    """Concrete DAO for storing Insight objects, herdando funcionalidades genéricas."""

    def __init__(self):
        super().__init__()

    def create(self, insight: Insight) -> Insight:
        """Salva um novo insight usando o método genérico."""
        data = {
            "id": insight.id,
            "indice": insight.indice,
            "recommendation": insight.recommendation
        }
        self._insert("insights", data)
        return insight

    def _map_row_to_insight(self, row) -> Insight:
        """Helper para converter linha do banco em objeto."""
        return Insight(
            id=row['id'], 
            indice=row['indice'], 
            recommendation=row['recommendation']
        )

    def find_by_id(self, insight_id: str) -> Insight | None:
        """Busca pelo ID usando o método genérico."""
        row = self._fetch_by_id("insights", insight_id)
        
        if row:
            return self._map_row_to_insight(row)
        return None

    def find_all(self) -> list[Insight]:
        """Busca todos os registros."""
        rows = self._fetch_all("insights")
        
        return [self._map_row_to_insight(row) for row in rows]

    def update(self, insight: Insight) -> Insight:
        """Atualiza os dados usando o método genérico."""
        data = {
            "indice": insight.indice,
            "recommendation": insight.recommendation
        }
        self._update("insights", insight.id, data)
        
        return insight

    def delete(self, insight_id: str) -> bool:
        """Deleta pelo ID usando o método genérico."""
        return self._delete("insights", insight_id)