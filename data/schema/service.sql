CREATE TABLE IF NOT EXISTS services (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    specialty_id TEXT,
    price REAL,
    FOREIGN KEY (specialty_id) REFERENCES specialties(id) ON DELETE SET NULL
);