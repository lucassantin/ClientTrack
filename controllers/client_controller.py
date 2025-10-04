from models.client import Client
import sqlite3

DB_NAME = "clienttrack.db"
class ClientController:
    def add(self, client: Client): ...