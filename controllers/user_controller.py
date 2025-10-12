from views.authentication_mod_view.user_view import UserView
from controllers.client_controller import ClientController
from controllers.employee_controller import EmployeeController

class UserController:
    """Controller principal do módulo de gerenciamento de usuários."""
    def __init__(self):
        self.view = UserView()
        self.client_controller = ClientController()
        self.employee_controller = EmployeeController()

    def iniciar(self):
        """Inicia o loop do menu de gerenciamento de usuários."""
        while True:
            opcao = self.view.exibir_menu_usuarios()
            
            if opcao == '1':
                self.client_controller.iniciar() 
            elif opcao == '2':
                self.employee_controller.iniciar() 
            elif opcao == '0':
                break 
            else:
                self.view.exibir_mensagem("Opção inválida.", sucesso=False)