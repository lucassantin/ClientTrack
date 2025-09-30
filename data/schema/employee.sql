CREATE TABLE IF NOT EXISTS employees (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    specialty_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (specialty_id) REFERENCES specialties(id)
)