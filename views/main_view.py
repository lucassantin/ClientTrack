import os

class MainView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu(self):
        print("========================================")
        print("      Bem-vindo ao TrackClients!")
        print("========================================\n")
        print("Escolha um dos módulos para gerenciar:")
        print("  1. Página de Gerenciamento")
        print("  2. Página de Usuários")
        print("\n  0. Sair do sistema")
        print("\n----------------------------------------")

    def obter_escolha(self) -> str:
        return input("Digite o número da sua escolha: ")

    def exibir_mensagem(self, msg: str):
        """Exibe uma mensagem de feedback para o usuário."""
        print(f"\n[AVISO] {msg}")
        input("Pressione Enter para continuar...")