import sqlite3
from models.specialty import Specialty

DB_NAME = "clienttrack.db"

class EspecialityController:
    def add(self): ...

    def get_all(self):
        sql = "select id, name, description from specialties"

        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(sql)

                rows = cursor.fetchall()

                specialties = [Specialty(specialty_id=row["id"], name=row["name"], description=row["description"]) for row in rows]

                return specialties
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []    
        

