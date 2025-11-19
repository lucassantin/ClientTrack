import sqlite3
from models.service import Service
from models.specialty import Specialty 

class ServiceSqliteDAO:
    def __init__(self):
        super().__init__()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path) 

    def create(self, service: Service) -> Service:
        specialty_id = service.specialty.id if service.specialty else None 
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO services (id, name, description, price, specialty_id) VALUES (?, ?, ?, ?, ?)",
                (service.id, service.name, service.description, service.price, specialty_id)
            )
            conn.commit()
        return service

    def _map_row_to_service(self, row: sqlite3.Row) -> Service:
        specialty = None
        if row['specialty_id'] is not None:
            specialty = Specialty(id=row['specialty_id'], name=row['specialty_name'], description=row['specialty_description'])
        
        return Service(id=row['id'], name=row['name'], description=row['description'], price=row['price'], specialty=specialty)

    def find_all(self) -> list[Service]:
        sql = """
            SELECT s.id, s.name, s.description, s.price, s.specialty_id, 
                   sp.name as specialty_name, sp.description as specialty_description
            FROM services s
            LEFT JOIN specialties sp ON s.specialty_id = sp.specialty_id 
        """
        services = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
            for row in rows:
                services.append(self._map_row_to_service(row))
        return services


    def update(self, service: Service) -> Service:
        specialty_id = service.specialty.id if service.specialty else None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE services SET name = ?, description = ?, price = ?, specialty_id = ? WHERE id = ?",
                (service.name, service.description, service.price, specialty_id, service.id)
            )
            conn.commit()
        return service

    def delete(self, service_id: str) -> bool:
        """Deletes a service by its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
            conn.commit()
            return cursor.rowcount > 0
    def find_by_id(self, service_id: str) -> Service | None:
        sql = """
            SELECT s.id, s.name, s.description, s.price, s.specialty_id, 
                   sp.name as specialty_name, sp.description as specialty_description
            FROM services s
            LEFT JOIN specialties sp ON s.specialty_id = sp.specialty_id
            WHERE s.id = ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (service_id,)).fetchone()
            if row:
                return self._map_row_to_service(row)
        return None