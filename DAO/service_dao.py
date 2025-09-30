import sqlite3
from models.service import Service

class ServiceSqliteDAO:
    """Concrete DAO for storing Service objects in a SQLite database."""

    def __init__(self, db_path: str):
        self.db_path = "clienttrack.db"
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def create(self, service: Service) -> Service:
        """Saves a new service to the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO services (id, name, description, price) VALUES (?, ?, ?, ?)",
                (service.id, service.name, service.description, service.price)
            )
            conn.commit()
        return service

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

    def find_all(self):
        """Returns a list of all services."""
        services = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM services")
            rows = cursor.fetchall()
            for row in rows:
                services.append(Service(id=row['id'], name=row['name'], description=row['description'], price=row['price']))
        return services

    def update(self, service: Service):
        """Updates an existing service."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE services SET name = ?, description = ?, price = ? WHERE id = ?",
                (service.name, service.description, service.price, service.id)
            )
            conn.commit()
        return self.find_by_id(service.id)

    def delete(self, service_id: str) -> bool:
        """Deletes a service by its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
            conn.commit()
            return cursor.rowcount > 0