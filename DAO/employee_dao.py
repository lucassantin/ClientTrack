import sqlite3
from models.employee import Employee
from models.user import User
from DAO.user_dao import UserSqliteDAO
from DAO.specialty_dao import SpecialtySqliteDAO

class EmployeeSqliteDAO:
    """DAO for Employee objects."""

    def __init__(self):
        self.db_path = "clienttrack.db"
        self.user_dao = UserSqliteDAO()
        self.specialty_dao = SpecialtySqliteDAO()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create(self, employee: Employee) -> Employee:
        self.user_dao.create(employee)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            specialty_id = employee.specialty.id if employee.specialty else None
            cursor.execute(
                "INSERT INTO employees (id, user_id, specialty_id) VALUES (?, ?, ?)",
                (employee.id, employee.user_id ,specialty_id)
            )
            conn.commit()
        return employee

    def find_by_id(self, employee_id: str):
        user = self.user_dao.find_by_id(employee_id)
        if not user:
            return None

        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
            employee_row = cursor.fetchone()
            if employee_row:
                specialty = self.specialty_dao.find_by_id(employee_row['specialty_id']) if employee_row['specialty_id'] else None
                user = self.user_dao.find_by_id(employee_row['user_id']) if employee_row['user_id'] else None
                if user:
                    user = User(user_id=user.user_id, name=user.name, contact=user.contact)
                return Employee(
                    user_id=user.user_id, id=employee_row['id'], name=user.name, contact=user.contact,
                    registered_at=user.registered_at, specialty=specialty
                )
        return None

    def find_all(self):
        employees = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.name, u.contact, u.registered_at, e.specialty_id
                FROM users u JOIN employees e ON u.id = e.id
                ORDER BY u.name
            """)
            rows = cursor.fetchall()
            for row in rows:
                specialty = self.specialty_dao.find_by_id(row['specialty_id']) if row['specialty_id'] else None
                user = self.user_dao.find_by_id(row['user_id']) if row['user_id'] else None
                if user:
                    user = User(user_id=user.user_id, name=user.name, contact=user.contact)
                employees.append(Employee(
                    user_id=user.user_id, id=row['id'], name=user.name, contact=user.contact,
                    registered_at=user.registered_at, specialty=specialty
                ))
        return employees

    def update(self, employee: Employee):
        self.user_dao.update(employee)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            specialty_id = employee.specialty.id if employee.specialty else None
            cursor.execute(
                "UPDATE employees SET specialty_id = ? WHERE id = ?",
                (specialty_id, employee.id)
            )
            conn.commit()
        return self.find_by_id(employee.id)

    def delete(self, employee_id: str) -> bool:
        # ON DELETE CASCADE handles deleting the employee record
        # when the corresponding user record is deleted.
        return self.user_dao.delete(employee_id)