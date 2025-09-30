CREATE TABLE IF NOT EXISTS employees (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    specialty_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (specialty_id) REFERENCES specialties(id)
)