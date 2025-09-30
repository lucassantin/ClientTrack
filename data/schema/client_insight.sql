CREATE TABLE IF NOT EXISTS client_insight (
    id TEXT PRIMARY KEY,
    client_id INTEGER NOT NULL,
    insight_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (insight_id) REFERENCES insights(id)
)