import os

class AppointmentMainView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu(self):
        self.limpar_tela()
        print("========= MENU DE Gerenciamento =========\n")
        print("Escolha uma das opções abaixo:")
        print("  1. Registrar tipo de pagamento")
        print("  2. Registrar serviços")
        print("  3. Registrar especialidades")
        print("  4. Registrar agendamento")
        print("\n  0. Voltar ao menu principal")
        print("\n========================================")

    def obter_opcao(self) -> str:
        """
        Apenas captura e retorna a entrada crua (string) do usuário.
        
        Returns:
            str: O texto que o usuário digitou.
        """
        return input("Digite o número da opção desejada: ")
