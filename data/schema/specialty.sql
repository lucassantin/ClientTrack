CREATE TABLE IF NOT EXISTS specialties (
    specialty_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);