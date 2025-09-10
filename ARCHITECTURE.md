# Project architecture

```
ClientTrack/
├── controllers/
│   ├── __init__.py
│   ├── appointment_controller.py
│   ├── client_controller.py
│   ├── employee_controller.py
│   ├── especiality_controller.py
│   ├── insight_controller.py
│   ├── payment_controller.py
│   ├── reports_controller.py
│   ├── service_controller.py
│   └── user_controller.py
│
├── models/
│   ├── __init__.py
│   ├── appointment.py
│   ├── client.py
│   ├── employee.py
│   ├── especiality.py
│   ├── insight.py
│   ├── payment.py
│   ├── service.py
│   └── user.py
│
├── utils/
│   ├── __init__.py
│   ├── exporter.py
│   ├── filters.py
│   ├── formatters.py
│   └── validators.py
│
├── views/
│   ├── __init__.py
│   └── cli_view.py
│
├── .gitignore
├── ARCHITECTURE.md
├── main.py
├── README.md
└── requirements.txt
```
