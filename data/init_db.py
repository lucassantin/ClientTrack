import _sqlite3

def init_db():
    conn = _sqlite3.connect('clienttrack.db')
    cursor = conn.cursor()

    # Create tables

    conn.commit()
    conn.close()