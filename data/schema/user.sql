CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    contact TEXT NOT NULL,
    registered_at TIMESTAMP
)