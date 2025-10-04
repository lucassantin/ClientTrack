# Em: DAO/service_dao.py
import sqlite3
from models.service import Service
from models.specialty import Specialty # Importar Specialty

class ServiceSqliteDAO:
    def __init__(self, db_path="clienttrack.db"):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path) 

    def create(self, service: Service) -> Service:
        specialty_id = service.specialty.id if service.specialty else None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO services (id, name, description, price, specialty_id) VALUES (?, ?, ?, ?, ?)",
                (service.id, service.name, service.description, service.price, specialty_id)
            )
            conn.commit()
        return service

    def _map_row_to_service(self, row: sqlite3.Row) -> Service:
        """Função auxiliar para mapear uma linha do DB para um objeto Service."""
        specialty = None
        if row['specialty_id'] is not None:
            specialty = Specialty(name=row['specialty_name'], 
                                  description=row['specialty_description'], 
                                  id=row['specialty_id'])
        
        service = Service(name=row['service_name'],
                          description=row['service_description'],
                          price=row['service_price'],
                          id=row['service_id'],
                          specialty=specialty)
        return service

    def find_all(self) -> list[Service]:
        services = []
        sql = """
            SELECT 
                s.id as service_id, s.name as service_name, s.description as service_description,
                s.price as service_price,
                sp.specialty_id as specialty_id, sp.name as specialty_name, sp.description as specialty_description
            FROM services s
            LEFT JOIN specialties sp ON s.specialty_id = sp.specialty_id
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute(sql).fetchall()
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
    def find_by_id(self, service_id: str):
        """Finds a service by its unique ID."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM services WHERE id = ?", (service_id,))
            row = cursor.fetchone()
            if row:
                return Service(id=row['id'], name=row['name'], description=row['description'], price=row['price'])
        return None