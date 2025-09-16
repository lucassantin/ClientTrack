import sqlite3
from models.insight import Insight

DB_NAME = "clienttrack.db"

class InsightController:
    def add(self, insight: Insight):
        sql = "insert into insights (indice, recommendation) values (?,?)"
        data_tuple = (insight.indice, insight.recommendation)

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, data_tuple)
                conn.commit()
                return cursor.lastrowid, None
        except sqlite3.Error as e:
            return None, e
        
    def get_all(self):
        sql = "select id, indice, recommendation from insights"

        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(sql)

                rows = cursor.fetchall()

                insights = [Insight(id=row["id"], indice=row["indice"], recommendation=row["recommendation"]) for row in rows]

                return insights, None
        except sqlite3.Error as e:
            return [], e
        
    def get(self, indice:int, recommendation: str):
        sql = 'select * from insights where indice = ? and recommendation = ?'

        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                row = cursor.execute(sql, (indice,recommendation)).fetchone()

                if row:
                    return Insight(id=row["id"], indice=row["indice"], recommendation=row["recommendation"])
                else:
                    return None
        except sqlite3.Error as e:
            return e