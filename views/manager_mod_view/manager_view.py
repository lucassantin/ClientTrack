import os

class AppointmentMainView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu(self):
        self.limpar_tela()
        print("========= MENU DE Gerenciamento =========\n")
        print("Escolha uma das opções abaixo:")
        print("  1. Pagamentos")
        print("  2. Serviços")
        print("  3. Especialidades")
        print("  4. Agendamentos")
        print("\n  0. Voltar ao menu principal")
        print("\n========================================")

    def obter_opcao(self) -> str:
        """
        Apenas captura e retorna a entrada crua (string) do usuário.
        
        Returns:
            str: O texto que o usuário digitou.
        """
        return input("Digite o número da opção desejada: ")
