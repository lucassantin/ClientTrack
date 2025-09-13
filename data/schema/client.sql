CREATE TABLE IF NOT EXISTS client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    birthday TEXT,
    insight_id INTEGER UNIQUE,
    accumulatedIndice INTEGER DEFAULT 0,
    FOREIGN KEY (insight_id) REFERENCES insights(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)