CREATE TABLE IF NOT EXISTS employees (
    id TEXT PRIMARY KEY,
    specialty_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (specialty_id) REFERENCES specialties(id) ON DELETE SET NULL
)