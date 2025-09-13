CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value FLOAT,
    typePayment_id INTEGER,
    FOREIGN KEY (typePayment_id) REFERENCES typePayments(id)
)