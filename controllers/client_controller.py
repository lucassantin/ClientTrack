from models.client import Client
import sqlite3

DB_NAME = "clienttrack.db"
class ClientController:
    def add(self, client: Client):
        sql = 'insert into clients (user_id, birthday, insight_id) values(?,?,?)'
        data_tuple = (client.user_id, client.birthDay, client.insight.id)

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, data_tuple)
                conn.commit()
                print(f"Client {client.name} added successfully")
                return True
        except sqlite3.Error as e:
            print(f"Error adding client {client.name}: {e}")
            return False
        
    def get_all(self):
        sql = """
        SELECT
            c.id AS client_id,
            c.birthday,
            u.id AS user_id,
            u.name,
            u.contact,
            i.indice,
            i.recommendation
        FROM
            clients AS c
        INNER JOIN
            users AS u ON u.id = c.user_id
        INNER JOIN
            insights AS i ON i.id = c.insight_id
        """

        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                rows = cursor.execute(sql).fetchall()

                clients = [
                    Client(
                        id=row["client_id"],
                        user_id=row["user_id"],
                        name=row["name"],
                        contact=row["contact"],
                        birthDay=row["birthday"],
                        indice=row["indice"],
                        recommendation=row["recommendation"]
                    ) for row in rows
                ]
                
                return clients
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []