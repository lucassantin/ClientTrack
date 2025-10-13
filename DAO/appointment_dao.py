print("--- CARREGANDO O ARQUIVO DAO/appointment_dao.py (VERSÃO CORRETA COM PRINTS) ---")

import sqlite3
from models.appointment import Appointment
from DAO.client_dao import ClientSqliteDAO
from DAO.service_dao import ServiceSqliteDAO
from DAO.employee_dao import EmployeeSqliteDAO
from DAO.payment_dao import PaymentSqliteDAO

class AppointmentSqliteDAO:
    def __init__(self):
        self.db_path = "clienttrack.db"
        self.client_dao = ClientSqliteDAO()
        self.service_dao = ServiceSqliteDAO()
        self.employee_dao = EmployeeSqliteDAO()
        self.payment_dao = PaymentSqliteDAO()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create(self, appointment: Appointment) -> Appointment:
        with self._get_connection() as conn:
            conn.execute(
                """INSERT INTO appointments (id, created_at, appointment_date, client_id, service_id, employee_id, payment_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (appointment.id, appointment.created_at, appointment.appointment_date,
                 appointment.client.id, appointment.service.id, 
                 appointment.employee.id, appointment.payment.id if appointment.payment else None)
            )
            conn.commit()
        return appointment

    def _map_row_to_appointment(self, row: sqlite3.Row) -> Appointment | None:
        """Cria um objeto Appointment a partir de uma linha do DB (com JOINs)."""
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
            print("estou aqui")
            for row in rows:
                print("entrei")
                appointment_obj = self._map_row_to_appointment(row)
                if appointment_obj:
                    appointments.append(appointment_obj)
        return appointments

    def find_by_id(self, appointment_id: str) -> Appointment | None:
        sql = "SELECT * FROM appointments WHERE id = ?"
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (appointment_id,)).fetchone()
            if row:
                return self._map_row_to_appointment(row)
        return None

    def delete(self, appointment_id: str) -> bool:
        with self._get_connection() as conn:
            rows_affected = conn.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,)).rowcount
            conn.commit()
            return rows_affected > 0
        
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