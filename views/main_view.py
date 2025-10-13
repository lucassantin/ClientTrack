import os

class MainView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu(self):
        print("========================================")
        print("      Bem-vindo ao TrackClients!")
        print("========================================\n")
        print("Escolha um dos módulos para gerenciar:")
        print("--- Gerenciamento ---")
        print("  1. Gerenciar Tipos de Pagamento")
        print("  2. Gerenciar Serviços")
        print("  3. Gerenciar Especialidades")
        print("  4. Gerenciar Agendamentos")
        print("\n--- Autenticação e Usuários ---")
        print("  5. Gerenciar Clientes")
        print("  6. Gerenciar Funcionários")
        print("\n----------------------------------------")
        print("  0. Sair do sistema")
        print("\n========================================")

    def obter_escolha(self) -> str:
        return input("Digite o número da sua escolha: ")

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe uma mensagem de feedback para o usuário."""
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")