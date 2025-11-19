import sqlite3
from DAO.dao import DAO
from models.appointment import Appointment
from DAO.client_dao import ClientSqliteDAO
from DAO.service_dao import ServiceSqliteDAO
from DAO.employee_dao import EmployeeSqliteDAO
from DAO.payment_dao import PaymentSqliteDAO

class AppointmentSqliteDAO(DAO):
    def __init__(self):
        super().__init__()
        self.client_dao = ClientSqliteDAO()
        self.service_dao = ServiceSqliteDAO()
        self.employee_dao = EmployeeSqliteDAO()
        self.payment_dao = PaymentSqliteDAO()

    def create(self, appointment: Appointment) -> Appointment:
        data = {
            "id": appointment.id,
            "created_at": appointment.created_at,
            "appointment_date": appointment.appointment_date,
            "client_id": appointment.client.id,
            "service_id": appointment.service.id,
            "employee_id": appointment.employee.id,
            "payment_id": appointment.payment.id if appointment.payment else None
        }
        self._insert("appointments", data)
        return appointment

    def _map_row_to_appointment(self, row: sqlite3.Row) -> Appointment | None:
        try:
            client = self.client_dao.find_by_id(row['client_id'])
            service = self.service_dao.find_by_id(row['service_id'])
            employee = self.employee_dao.find_by_id(row['employee_id'])
            payment = self.payment_dao.find_by_id(row['payment_id']) if row['payment_id'] else None

            if not all([client, service, employee]):
                return None 

            return Appointment(
                id=row['id'],
                created_at=row['created_at'],
                appointment_date=row['appointment_date'],
                client=client,
                service=service,
                employee=employee,
                payment=payment
            )
        except Exception:
            return None

    def find_all(self) -> list[Appointment]:
        sql = "SELECT * FROM appointments ORDER BY appointment_date DESC"
        
        appointments = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
            for row in rows:
                appointment_obj = self._map_row_to_appointment(row)
                if appointment_obj:
                    appointments.append(appointment_obj)
        return appointments

    def find_by_id(self, appointment_id: str) -> Appointment | None:
        row = self._fetch_by_id("appointments", appointment_id)
        if row:
            return self._map_row_to_appointment(row)
        return None

    def update(self, appointment: Appointment) -> Appointment:
        data = {
            "appointment_date": appointment.appointment_date,
            "service_id": appointment.service.id,
            "employee_id": appointment.employee.id,
            "payment_id": appointment.payment.id if appointment.payment else None
        }
        self._update("appointments", appointment.id, data)
        return appointment

    def delete(self, appointment_id: str) -> bool:
        return self._delete("appointments", appointment_id)

    def get_most_used_services(self, limit: int = 5) -> list[dict]:
        sql = """
            SELECT s.name, COUNT(a.service_id) as total
            FROM appointments a
            JOIN services s ON a.service_id = s.id
            GROUP BY s.name
            ORDER BY total DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(sql, (limit,)).fetchall()

    def get_most_frequent_clients(self, limit: int = 5) -> list[dict]:
        sql = """
            SELECT u.name, COUNT(a.client_id) as total
            FROM appointments a
            JOIN users u ON a.client_id = u.id
            GROUP BY u.name
            ORDER BY total DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(sql, (limit,)).fetchall()

    def get_busiest_employees(self, limit: int = 5) -> list[dict]:
        sql = """
            SELECT u.name, COUNT(a.employee_id) as total
            FROM appointments a
            JOIN users u ON a.employee_id = u.id
            GROUP BY u.name
            ORDER BY total DESC
            LIMIT ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(sql, (limit,)).fetchall()

    def get_inactive_clients(self) -> list[dict]:
        sql = """
            SELECT 
                u.name,
                u.contact,
                MAX(a.appointment_date) as last_appointment,
                CAST(julianday('now') - julianday(MAX(a.appointment_date)) AS INTEGER) as days_since_last
            FROM users u
            JOIN clients c ON u.id = c.id
            LEFT JOIN appointments a ON u.id = a.client_id
            GROUP BY u.id
            ORDER BY days_since_last DESC
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(sql).fetchall()