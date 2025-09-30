CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    value FLOAT,
    date_time DATETIMES
    typePayment_id INTEGER,
    FOREIGN KEY (typePayment_id) REFERENCES typePayments(id)
)