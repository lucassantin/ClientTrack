CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    value REAL,
    date_time TEXT DEFAULT (datetime('now', 'localtime')),
    typePayment_id TEXT,
    FOREIGN KEY (typePayment_id) REFERENCES payment_types(id) ON DELETE SET NULL
)