import sqlite3
from models.appointment import Appointment

from DAO.service_dao import ServiceSqliteDAO
from DAO.employee_dao import EmployeeSqliteDAO
from DAO.payment_dao import PaymentSqliteDAO

class AppointmentSqliteDAO:
    """Concrete DAO for storing Appointment objects in a SQLite database."""

    def __init__(self, db_path: str):
        self.db_path = "clienttrack.db"
        self.service_dao = ServiceSqliteDAO()
        self.employee_dao = EmployeeSqliteDAO(db_path)
        self.payment_dao = PaymentSqliteDAO()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def create(self, appointment: Appointment) -> Appointment:
        """Saves a new appointment, storing foreign keys."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO appointments (id, created_at, appointment_date, service_id, employee_id, payment_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    appointment.id,
                    appointment.created_at,
                    appointment.appointment_date,
                    appointment.service.id,
                    appointment.employee.id,
                    appointment.payment.id
                )
            )
            conn.commit()
        return appointment

    def find_by_id(self, appointment_id: str):
        """Finds an appointment and reconstructs it with all related objects."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
            row = cursor.fetchone()
            if row:
                service = self.service_dao.find_by_id(row['service_id'])
                employee = self.employee_dao.find_by_id(row['employee_id'])
                payment = self.payment_dao.find_by_id(row['payment_id'])

                if service and employee and payment:
                    return Appointment(
                        id=row['id'],
                        created_at=row['created_at'],
                        appointment_date=row['appointment_date'],
                        service=service,
                        employee=employee,
                        payment=payment
                    )
        return None

    def find_all(self):
        """Returns a list of all appointments with their related objects."""
        appointments = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments ORDER BY appointment_date DESC")
            rows = cursor.fetchall()
            for row in rows:
                service = self.service_dao.find_by_id(row['service_id'])
                employee = self.employee_dao.find_by_id(row['employee_id'])
                payment = self.payment_dao.find_by_id(row['payment_id'])
                if service and employee and payment:
                    appointments.append(Appointment(
                        id=row['id'],
                        created_at=row['created_at'],
                        appointment_date=row['appointment_date'],
                        service=service,
                        employee=employee,
                        payment=payment
                    ))
        return appointments

    def update(self, appointment: Appointment):
        """Updates an existing appointment."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE appointments
                SET appointment_date = ?, service_id = ?, employee_id = ?, payment_id = ?
                WHERE id = ?
                """,
                (
                    appointment.appointment_date,
                    appointment.service.id,
                    appointment.employee.id,
                    appointment.payment.id,
                    appointment.id
                )
            )
            conn.commit()
        return self.find_by_id(appointment.id)

    def delete(self, appointment_id: str) -> bool:
        """Deletes an appointment by its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            conn.commit()
            return cursor.rowcount > 0