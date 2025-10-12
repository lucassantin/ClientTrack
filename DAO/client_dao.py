import sqlite3
from models.client import Client
from models.insight import Insight
from DAO.user_dao import UserSqliteDAO

class ClientSqliteDAO:
    """DAO para objetos Client, seguindo o padrão de Composição para Insight."""

    def __init__(self, db_path="clienttrack.db"):
        self.db_path = db_path
        self.user_dao = UserSqliteDAO(db_path)

    def _get_connection(self) -> sqlite3.Connection:
        """Estabelece uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_path)

    def create(self, client: Client) -> Client:
        """Salva um novo cliente nas tabelas 'users' e 'clients'."""
        self.user_dao.create(client)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO clients 
                   (id, birthday, accumulatedIndice, insight_indice, insight_recommendation) 
                   VALUES (?, ?, ?, ?, ?)""",
                (client.id, client.birthDay, client.accumulatedIndice, 
                 client.insight.indice, client.insight.recommendation)
            )
            conn.commit()
        return client

    def _map_row_to_client(self, row: sqlite3.Row) -> Client:
        """Cria um objeto Client a partir de uma linha do banco de dados."""
        return Client(
            id=row['id'],
            name=row['name'],
            contact=row['contact'],
            registered_at=row['registered_at'],
            birthDay=row['birthday'],
            accumulatedIndice=row['accumulatedIndice'],
            indice=row['insight_indice'],
            recommendation=row['insight_recommendation']
        )

    def find_all(self) -> list[Client]:
        """Busca todos os clientes juntando dados das tabelas users e clients."""
        sql = """
            SELECT u.*, c.birthday, c.accumulatedIndice, c.insight_indice, c.insight_recommendation 
            FROM users u JOIN clients c ON u.id = c.id
        """
        clients = []
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
            for row in rows:
                clients.append(self._map_row_to_client(row))
        return clients

    def find_by_id(self, client_id: str) -> Client | None:
        """Busca um cliente específico pelo seu ID."""
        sql = """
            SELECT u.*, c.birthday, c.accumulatedIndice, c.insight_indice, c.insight_recommendation 
            FROM users u JOIN clients c ON u.id = c.id 
            WHERE u.id = ?
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (client_id,)).fetchone()
            if row:
                return self._map_row_to_client(row)
        return None

    def update(self, client: Client) -> Client:
        """Atualiza os dados de um cliente nas tabelas 'users' e 'clients'."""
        self.user_dao.update(client)
        with self._get_connection() as conn:
            conn.execute(
                """UPDATE clients SET 
                   birthday = ?, accumulatedIndice = ?, insight_indice = ?, insight_recommendation = ? 
                   WHERE id = ?""",
                (client.birthDay, client.accumulatedIndice, 
                 client.insight.indice, client.insight.recommendation, client.id)
            )
            conn.commit()
        return client

    def update_indice(self, client_id: str, new_indice: int):
        """Método específico para atualizar apenas o índice acumulado de um cliente."""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE clients SET accumulatedIndice = ? WHERE id = ?",
                (new_indice, client_id)
            )
            conn.commit()

    def delete(self, client_id: str) -> bool:
        """Deleta um cliente (e usuário correspondente) do banco de dados."""
        return self.user_dao.delete(client_id)