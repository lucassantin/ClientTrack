
from views.main_view import MainView
from controllers.gerenciamento_controller import GerenciamentoController

class MainController:
    def __init__(self):
        self.main_view = MainView()
        self.gerenciamento_controller = GerenciamentoController()

    def iniciar(self):
        try:
            while True:
                self.main_view.limpar_tela()
                self.main_view.exibir_menu()
                command = self.main_view.obter_escolha()

                if command == "1":
                    self.gerenciamento_controller.iniciar()
                
                elif command == "2":
                    self.main_view.exibir_mensagem("Módulo de Usuários não implementado.")

                elif command == "0":
                    break 

                else:
                    self.main_view.exibir_mensagem("Opção inválida, tente novamente.")
        
        except KeyboardInterrupt:
            return self.main_view.exibir_mensagem(msg="Programa encerrado pelo usuário.")