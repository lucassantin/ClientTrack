CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY,
    birthday TEXT,
    accumulatedIndice INTEGER DEFAULT 0,
    insight_indice INTEGER, 
    insight_recommendation TEXT,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
)