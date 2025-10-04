import os
from models.payment_type import PaymentType

class PaymentView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_gerenciamento(self) -> str:
        self.limpar_tela()
        print("====== GERENCIAR TIPOS DE PAGAMENTO ======\n")
        print("  1. Listar todos os tipos")
        print("  2. Adicionar novo tipo")
        print("  3. Atualizar um tipo existente")
        print("  4. Deletar um tipo")
        print("\n  0. Voltar ao menu anterior")
        print("\n==========================================")
        return input("Escolha uma opção: ")

    def obter_dados_tipo_pagamento(self) -> dict:
        self.limpar_tela()
        print("====== ADICIONAR NOVO TIPO DE PAGAMENTO ======\n")
        print("(Deixe o nome em branco e pressione Enter para cancelar)\n")
        nome = input("Nome (ex: Cartão de Crédito, Dinheiro): ")
        return {"nome": nome}

    def exibir_lista_tipos_pagamento(self, tipos: list):
        self.limpar_tela()
        print("====== LISTA DE TIPOS DE PAGAMENTO ======\n")
        if not tipos:
            print("Nenhum tipo de pagamento cadastrado.")
        else:
            for i, tipo in enumerate(tipos):
                print(f"  {i + 1}. {tipo.name} (ID: {tipo.id})")
        print("\n=========================================")
        input("Pressione Enter para continuar...")
        
    def obter_escolha_tipo(self, tipos: list, acao: str) -> PaymentType | None:
        """Pede ao usuário para escolher um tipo da lista para uma ação."""
        self.limpar_tela()
        print(f"====== SELECIONE UM TIPO PARA {acao.upper()} ======\n")
        if not tipos:
            print("Nenhum tipo de pagamento para selecionar.")
            input("\nPressione Enter para voltar...")
            return None
            
        for i, tipo in enumerate(tipos):
            print(f"  {i + 1}. {tipo.name}")
        print("\n  0. Cancelar")
        print("\n================================================")

        while True:
            try:
                escolha = int(input("Digite o número do tipo: "))
                if 0 <= escolha <= len(tipos):
                    return None if escolha == 0 else tipos[escolha - 1]
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    def obter_novos_dados_para_atualizar(self, tipo_antigo: PaymentType) -> dict:
        """Pede o novo nome para um tipo de pagamento."""
        self.limpar_tela()
        print(f"====== ATUALIZANDO '{tipo_antigo.name}' ======\n")
        print("(Deixe em branco e pressione Enter para cancelar)\n")
        novo_nome = input(f"Digite o novo nome para '{tipo_antigo.name}': ")
        return {"nome": novo_nome}

    def confirmar_exclusao(self, nome_tipo: str) -> bool:
        """Pede confirmação do usuário antes de deletar."""
        self.limpar_tela()
        print(f"====== CONFIRMAR EXCLUSÃO ======\n")
        confirmacao = input(f"Tem certeza que deseja deletar '{nome_tipo}'? (s/n): ").lower()
        return confirmacao == 's'

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe uma mensagem de feedback."""
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")