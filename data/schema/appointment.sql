CREATE TABLE IF NOT EXISTS appointments (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    appointment_date DATETIME,
    service_id INTEGER,
    employee_id INTEGER,
    payment_id INTEGER,
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (payment_id) REFERENCES payments(id)
);