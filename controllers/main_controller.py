from views.main_view import MainView

from controllers.payment_controller import PaymentController
from controllers.service_controller import ServiceController
from controllers.especiality_controller import EspecialityController
from controllers.appointment_controller import AppointmentController
from controllers.client_controller import ClientController
from controllers.employee_controller import EmployeeController
from controllers.report_controller import ReportController

class MainController:
    """
    O Controller principal e unificado da aplicação.
    Gerencia a navegação e delega as ações para os controllers especializados.
    """
    def __init__(self):
        self.main_view = MainView()
        
        self.payment_controller = PaymentController()
        self.service_controller = ServiceController()
        self.especiality_controller = EspecialityController()
        self.appointment_controller = AppointmentController()
        self.client_controller = ClientController()
        self.employee_controller = EmployeeController()
        self.report_controller = ReportController()

    def iniciar(self):
        """Inicia o loop principal da aplicação com o menu unificado."""
        while True:
            escolha = self.main_view.exibir_menu()

            match escolha:
                case '1': self.payment_controller.gerenciar()
                case '2': self.service_controller.iniciar()
                case '3': self.especiality_controller.iniciar()
                case '4': self.appointment_controller.iniciar()
                case '5': self.client_controller.iniciar()
                case '6': self.employee_controller.iniciar()
                case '7': self.report_controller.iniciar()
                case '0':
                    print("\nSaindo do sistema. Até logo!")
                    break 
                case _:
                    self.main_view.exibir_mensagem("Opção inválida, tente novamente.", sucesso=False)