import os

class UserView:
    """View para o menu principal do módulo de usuários."""
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_usuarios(self) -> str:
        self.limpar_tela()
        print("====== GERENCIAR USUÁRIOS ======\n")
        print("  1. Gerenciar Clientes")
        print("  2. Gerenciar Funcionários")
        print("\n  0. Voltar ao menu anterior")
        print("\n==============================")
        return input("Escolha uma opção: ")

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")