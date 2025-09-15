from models.employee import Employee
from models.client import Client
from models.user import User
from models.insight import Insight

from controllers.user_controller import UserController
from controllers.employee_controller import EmployeeController
from controllers.client_controller import ClientController
from controllers.especiality_controller import EspecialityController
from controllers.insight_controller import InsightController

class employeeView:
    def __init__(self):
        self.controller = EmployeeController()

    def create(self):
        """Create a new employee."""
        especialites = EspecialityController().get_all()
        if  especialites == []: 
            return print("Please, before proceeding create a specialty\n")     

        name = input("Name:")
        contact = input("Contact:")

        print()
        print("-----Especialites-----")
        print()
        for especialty in especialites:
            print(f"ID: {especialty.specialty_id}, Name: {especialty.name}, Description: {especialty.description}")
        print()

        specialty = int(input("Specialty(id):"))
        
        for especialty in especialites:
            if especialty.specialty_id == int(specialty):
                specialty_obj = especialty
                break

        employee = Employee(name=name, contact=contact, specialty=specialty_obj)
        self.controller.add(employee=employee)

    def read(self): ...
    def update(self): ...
    def delete(self): ...

class clientView:
    def __init__(self):
        self.controller = ClientController()

    def create(self):
        name = input("Name:")
        contact = input("Contact:")
        user = User(name=name, contact=contact)
        user_id = UserController().add(user)
        if not user_id: 
            print("Failed to create user.")
            return

        birthday = input("Birthday (YYYY-MM-DD):")

        print("To create a insight")
        indice = int(input("Indice:"))
        recommendation = input("Recommendation:")
        insight = Insight(indice=indice, recommendation=recommendation)
        insight_id = InsightController().add(insight=insight)
        if not insight_id:
            print("Error to create insight")
            return
        
        client = Client(
            name=name, 
            contact=contact, 
            birthDay=birthday, 
            indice=indice, 
            recommendation=recommendation,
            user_id=user_id
        )
        client.insight.id=insight_id
        self.controller.add(client)



    def get_all(self):
        all_clients = self.controller.get_all()

        if all_clients:
            print("\n-----All clients-----")
            print()
            for client in all_clients:
                print(f"ID: {client.id}, Name: {client.name}, Contact: {client.contact}, Birthday: {client.birthDay}")
            print()
        else:
            print("\nNo clients found in the database")