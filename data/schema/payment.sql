CREATE TABLE IF NOT EXISTS payments (
    id FOREIGN KEY INTEGER AUTOINCREMENT,
    value FLOAT,
    typePayment_id INTEGER,
    FOREIGN KEY (typePayment_id) REFERENCES typePayments(id)
)s