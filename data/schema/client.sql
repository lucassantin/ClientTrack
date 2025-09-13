CREATE TABLE IF NOT EXISTS client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    birthday TEXT,
    insight_id INTEGER UNIQUE,
    FOREIGN KEY (insight_id) REFERENCES insights(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)