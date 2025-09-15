import sqlite3
import os


def initialize_database():
    DB_NAME = "clienttrack.db"
    SCHEMA_DIR = "data/schema"

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            print("Running the scripts of schema...")

            sql_files = [f for f in os.listdir(SCHEMA_DIR) if f.endswith('.sql')]
            
            for sql_file in sorted(sql_files):
                filepath = os.path.join(SCHEMA_DIR, sql_file)
                with open(filepath, 'r') as f:
                    sql_script = f.read()
                    cursor.executescript(sql_script) 
                print(f" - Script '{sql_file}' executed.")

            conn.commit()
            print("Data base start with sucess.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    initialize_database()