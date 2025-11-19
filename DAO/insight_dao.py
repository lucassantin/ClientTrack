import sqlite3
from DAO.dao import DAO
from models.insight import Insight

class InsightSqliteDAO(DAO):
    """Concrete DAO for storing Insight objects in a SQLite database."""

    def __init__(self):
        super().__init__()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(self._db_path)

    def create(self, insight: Insight) -> Insight:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO insights (id, indice, recommendation) VALUES (?, ?, ?)",
                (insight.id, insight.indice, insight.recommendation)
            )
            conn.commit()
        return insight

    def find_by_id(self, insight_id: str):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM insights WHERE id = ?", (insight_id,))
            row = cursor.fetchone()
            if row:
                return Insight(id=row['id'], indice=row['indice'], recommendation=row['recommendation'])
        return None

    def find_all(self):
        insights = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM insights")
            rows = cursor.fetchall()
            for row in rows:
                insights.append(Insight(id=row['id'], indice=row['indice'], recommendation=row['recommendation']))
        return insights

    def update(self, insight: Insight):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE insights SET indice = ?, recommendation = ? WHERE id = ?",
                (insight.indice, insight.recommendation, insight.id)
            )
            conn.commit()
        return self.find_by_id(insight.id)

    def delete(self, insight_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM insights WHERE id = ?", (insight_id,))
            conn.commit()
            return cursor.rowcount > 0