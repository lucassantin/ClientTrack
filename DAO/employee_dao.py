import sqlite3
from models.employee import Employee
from models.specialty import Specialty
from DAO.user_dao import UserSqliteDAO
from DAO.specialty_dao import SpecialtySqliteDAO

class EmployeeSqliteDAO:
    """DAO para objetos Employee, lida com as tabelas users e employees."""

    def __init__(self):
        self.db_path = "clienttrack.db"
        self.user_dao = UserSqliteDAO()
        self.specialty_dao = SpecialtySqliteDAO()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create(self, employee: Employee) -> Employee:
        self.user_dao.create(employee)
        with self._get_connection() as conn:
            specialty_id = employee.specialty.id if employee.specialty else None
            conn.execute(
                "INSERT INTO employees (id, specialty_id) VALUES (?, ?)",
                (employee.id, specialty_id)
            )
            conn.commit()
        return employee

    def _map_row_to_employee(self, row: sqlite3.Row) -> Employee:
        """Cria um objeto Employee a partir de uma linha do banco (resultado de um JOIN)."""
        specialty = None
        if row['specialty_id'] is not None and 'specialty_name' in row.keys():
            specialty = Specialty(
                id=row['specialty_id'],
                name=row['specialty_name'],
                description=row['specialty_description']
            )
        
        return Employee(
            id=row['id'],
            name=row['name'],
            contact=row['contact'],
            registered_at=row['registered_at'],
            specialty=specialty
        )

    def find_all(self) -> list[Employee]:
        sql = """
            SELECT u.*, e.specialty_id, s.name as specialty_name, s.description as specialty_description
            FROM users u 
            JOIN employees e ON u.id = e.id
            LEFT JOIN specialties s ON e.specialty_id = s.specialty_id
        """
        employees = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
            for row in rows:
                employees.append(self._map_row_to_employee(row))
        return employees
    
    def find_by_id(self, employee_id: str) -> Employee | None:
        """Busca um funcionário específico pelo seu ID."""
        sql = """
            SELECT u.*, e.specialty_id, s.name as specialty_name, s.description as specialty_description
            FROM users u 
            JOIN employees e ON u.id = e.id
            LEFT JOIN specialties s ON e.specialty_id = s.specialty_id 
            WHERE u.id = ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (employee_id,)).fetchone()
            if row:
                return self._map_row_to_employee(row)
        return None

    def update(self, employee: Employee) -> Employee:
        self.user_dao.update(employee)
        with self._get_connection() as conn:
            specialty_id = employee.specialty.id if employee.specialty else None
            conn.execute(
                "UPDATE employees SET specialty_id = ? WHERE id = ?",
                (specialty_id, employee.id)
            )
            conn.commit()
        return employee

    def delete(self, employee_id: str) -> bool:
        return self.user_dao.delete(employee_id)