import sqlite3
from models.employee import Employee
from models.specialty import Specialty
from DAO.user_dao import UserSqliteDAO
from DAO.specialty_dao import SpecialtySqliteDAO
from DAO.dao import DAO

class EmployeeSqliteDAO(DAO):
    """DAO para objetos Employee, lida com as tabelas users e employees."""

    def __init__(self):
        super().__init__()
        self.user_dao = UserSqliteDAO()
        self.specialty_dao = SpecialtySqliteDAO()

    def create(self, employee: Employee) -> Employee:
        """Salva um novo funcionário."""
        self.user_dao.create(employee)
        
        specialty_id = employee.specialty.id if employee.specialty else None
        
        data = {
            "id": employee.id,
            "specialty_id": specialty_id 
        }
        
        self._insert("employees", data)
        return employee

    def _map_row_to_employee(self, row) -> Employee:
        """Converte linha do banco em objeto Employee, buscando a Especialidade."""
        specialty = None
        
        if row['specialty_id']:
            specialty = self.specialty_dao.find_by_id(row['specialty_id'])
        
        return Employee(
            id=row['id'],
            name=row['name'],
            contact=row['contact'],
            registered_at=row['registered_at'],
            specialty=specialty
        )

    def find_all(self) -> list[Employee]:
        """Busca todos os funcionários (fazendo JOIN com users)."""
        sql = """
            SELECT u.*, e.specialty_id 
            FROM users u 
            JOIN employees e ON u.id = e.id
        """
        
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
            return [self._map_row_to_employee(row) for row in rows]
    
    def find_by_id(self, employee_id: str) -> Employee | None:
        """Busca um funcionário específico pelo ID."""
        sql = """
            SELECT u.*, e.specialty_id 
            FROM users u 
            JOIN employees e ON u.id = e.id
            WHERE u.id = ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (employee_id,)).fetchone()
            if row:
                return self._map_row_to_employee(row)
        return None

    def update(self, employee: Employee) -> Employee:
        """Atualiza os dados do funcionário."""
        self.user_dao.update(employee)
        
        specialty_id = employee.specialty.id if employee.specialty else None
        
        data = {
            "specialty_id": specialty_id
        }
        
        self._update("employees", employee.id, data)
        return employee

    def delete(self, employee_id: str) -> bool:
        """Deleta o funcionário (e usuário)."""
        return self.user_dao.delete(employee_id)