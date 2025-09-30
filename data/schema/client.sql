CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    birthday TEXT,
    insight_id INTEGER UNIQUE,
    accumulatedIndice INTEGER DEFAULT 0,
    FOREIGN KEY (insight_id) REFERENCES insights(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)