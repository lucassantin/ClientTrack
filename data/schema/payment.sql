CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    value FLOAT,
    typePayment_id INTEGER,
    FOREIGN KEY (typePayment_id) REFERENCES typePayments(id)
)