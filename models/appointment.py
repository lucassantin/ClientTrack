import datetime
from models.service import Service
from models.employee import Employee
from models.payment import Payment

class Appointment:
    def __init__(self, appointment_date: str,service: Service, employee: Employee, payment: Payment):
        self.__created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__appointment_date = None
        self.__service = None
        self.__employee = None
        self.__payment = None

        if isinstance(appointment_date, str):
            try:
                datetime.datetime.strptime(appointment_date, "%Y-%m-%d %H:%M")
                self.__appointment_date = appointment_date
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD HH:MM.")

        if isinstance(service, Service):
            self.__service = service

        if isinstance(employee, Employee):
            self.__employee = employee

        if isinstance(payment, Payment):
            self.__payment = payment


    @property
    def created_at(self) -> str:
        return self.__created_at

    @property
    def appointment_date(self) -> str:
        return self.__appointment_date
    
    @appointment_date.setter
    def appointment_date(self, appointment_date: str):
        if isinstance(appointment_date, str):
            try:
                datetime.datetime.strptime(appointment_date, "%Y-%m-%d %H:%M")
                self.__appointment_date = appointment_date
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD HH:MM.")
        else:
            raise TypeError("Appointment date must be a string in YYYY-MM-DD HH:MM format")

    @property
    def service(self) -> Service:
        return self.__service
    
    @service.setter
    def service(self, service: Service):
        if isinstance(service, Service):
            self.__service = service
        else:
            raise TypeError("Service must be an instance of Service")

    @property
    def employee(self) -> Employee:
        return self.__employee

    @employee.setter
    def employee(self, employee: Employee):
        if isinstance(employee, Employee):
            self.__employee = employee
        else:
            raise TypeError("Employee must be an instance of Employee")
    
    @property
    def payment(self) -> Payment:
        return self.__payment

    @payment.setter
    def payment(self, payment: Payment):
        if isinstance(payment, Payment):
            self.__payment = payment
        else:
            raise TypeError("Payment must be an instance of Payment")
