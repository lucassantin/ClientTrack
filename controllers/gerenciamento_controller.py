from views.manager_mod_view.manager_view import AppointmentMainView

from controllers.payment_controller import PaymentController
from controllers.appointment_controller import AppointmentController
from controllers.service_controller import ServiceController
from controllers.especiality_controller import EspecialityController

class GerenciamentoController:
    """
    Controller intermediário que gerencia o sub-menu de "Gerenciamento".
    Ele delega as ações para controllers mais especializados.
    """
    def __init__(self):
        self.view = AppointmentMainView()
        
        self.payment_controller = PaymentController()
        self.appointment_controller = AppointmentController()
        self.services_controller = ServiceController()
        self.especiality_controller = EspecialityController()

    def iniciar(self):
        while True:
            self.view.exibir_menu()
            opcao = self.view.obter_opcao()

            
            
            match opcao:
                case '1':
                    self.payment_controller.gerenciar()

                case '2':
                    self.services_controller.iniciar()

                case '3':
                    self.especiality_controller.iniciar()
                    
                case '4':
                    self.appointment_controller.iniciar()
                
                case '0':
                    break

                case _:
                    self.view.exibir_mensagem("Opção inválida, tente novamente.")
                    input("Pressione Enter para continuar...")