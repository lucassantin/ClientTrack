import sqlite3
from models.specialty import Specialty

class SpecialtySqliteDAO:
    """Concrete DAO for storing Specialty objects in a SQLite database."""

    def __init__(self):
        self.db_path = "clienttrack.db"

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def create(self, specialty: Specialty) -> Specialty:
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO specialties (specialty_id, name, description) VALUES (?, ?, ?)",
                (specialty.id, specialty.name, specialty.description) 
            )
            conn.commit()
        return specialty

    def find_by_id(self, specialty_id: str) -> Specialty | None:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM specialties WHERE specialty_id = ?", (specialty_id,)).fetchone()
            if row:
                return Specialty(id=row['specialty_id'], name=row['name'], description=row['description'])
        return None

    def find_all(self) -> list[Specialty]:
        specialties = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM specialties").fetchall()
            for row in rows:
                specialties.append(Specialty(id=row['specialty_id'], name=row['name'], description=row['description']))
        return specialties

    def update(self, specialty: Specialty):
        """Updates an existing specialty."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE specialties SET name = ?, description = ? WHERE specialty_id = ?",
                (specialty.name, specialty.description, specialty.id)
            )
            conn.commit()
        return self.find_by_id(specialty.id)

    def delete(self, specialty_id: str) -> bool:
        """Deletes a specialty by its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM specialties WHERE specialty_id = ?", (specialty_id,))
            conn.commit()
            return cursor.rowcount > 0