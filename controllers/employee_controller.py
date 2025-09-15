import sqlite3
from models.employee import Employee


DB_NAME = "clienttrack.db"
class EmployeeController:
    def add(self, employee: Employee):
        sql = "insert into employees (user_id, specialty_id) values (?,?)"
        data_tuple = (employee.user_id, employee.employee_id)

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(sql,data_tuple)
                conn.commit()
                print(f"Employee {employee.name} added successfully")
                return True
        except sqlite3.Error as e:
            print(f"Error adding employee: {e}")
            return False

    def get_all(self): ...