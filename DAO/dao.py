import sqlite3
from typing import Any, Dict, List, Optional

class DAO:
    def __init__(self):
        self._cache = {} 
        self._db_path = "clienttrack.db"

    def _get_connection(self) -> sqlite3.Connection:
        """Cria conexão configurada para acessar colunas por nome."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row 
        return conn

    def _insert(self, table_name: str, data: Dict[str, Any]) -> str:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = list(data.values())
        
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
            
            if 'id' in data:
                self._cache[data['id']] = data
                return data['id']
            return str(cursor.lastrowid)

    def _fetch_by_id(self, table_name: str, id_value: Any) -> Optional[sqlite3.Row]:

        sql = f"SELECT * FROM {table_name} WHERE id = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_value,))
            row = cursor.fetchone()
            
            if row:
                return row
        return None

    def _fetch_all(self, table_name: str) -> List[sqlite3.Row]:
        sql = f"SELECT * FROM {table_name}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def _update(self, table_name: str, id_value: Any, data: Dict[str, Any]) -> None:
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = list(data.values())
        values.append(id_value)
        
        sql = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()

        if id_value in self._cache:
             self._cache[id_value].update(data)

    def _delete(self, table_name: str, id_value: Any) -> bool:
        sql = f"DELETE FROM {table_name} WHERE id = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_value,))
            conn.commit()
            deleted = cursor.rowcount > 0
        
        if deleted and id_value in self._cache:
            del self._cache[id_value]
            
        return deleted