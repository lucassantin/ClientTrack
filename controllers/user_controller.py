import sqlite3
from models.user import User

DB_NAME = "clienttrack.db"

class UserController:
    def add(self, user: User):
        sql = "insert into users (name, contact) values (?,?)"
        data_tuple = (user.name, user.contact)

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, data_tuple)
                conn.commit()
                return cursor.lastrowid, True
        except sqlite3.Error as e:
            return False, e
    

