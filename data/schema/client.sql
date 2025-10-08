CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    birthday TEXT,
    insight_id INTEGER UNIQUE,
    accumulatedIndice INTEGER DEFAULT 0,
    FOREIGN KEY (insight_id) REFERENCES insights(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)