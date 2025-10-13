import os
from models.client import Client

class ClientView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_clientes(self) -> str:
        self.limpar_tela()
        print("======= GERENCIAR CLIENTES E FIDELIDADE =======\n")
        print("  1. Listar todos os clientes")
        print("  2. Adicionar novo cliente")
        print("  3. Atualizar um cliente")
        print("  4. Deletar um cliente")
        print("  5. Verificar Pontuação/Insight de um Cliente")
        print("  6. Resgatar Insight para um Cliente")
        print("\n  0. Voltar")
        print("\n=============================================")
        return input("Escolha uma opção: ")

    def obter_dados_cliente(self) -> dict:
        self.limpar_tela()
        print("====== ADICIONAR NOVO CLIENTE ======\n")
        name = input("Nome: ")
        if not name.strip(): return {}
        
        contact = input("Contato (Telefone/Email): ")
        birthDay = input("Data de Nascimento (AAAA-MM-DD, opcional): ")
        
        print("\n--- Dados para o Insight Padrão ---")
        indice = input("Nº de agendamentos para ganhar recomendação (ex: 5): ")
        recommendation = input("Texto da recomendação/insight: ")

        return {
            "name": name, "contact": contact, "birthDay": birthDay,
            "indice": indice, "recommendation": recommendation
        }

    def exibir_lista_clientes(self, clientes: list[Client]):
        self.limpar_tela()
        print("===================== LISTA DE CLIENTES =====================\n")
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            print(f"{'#':<3} {'NOME':<25} {'CONTATO':<20} {'ANIVERSÁRIO':<12} {'PONTOS':<8} {'META'}")
            print("-" * 80)
            
            for i, cliente in enumerate(clientes):
                birthday_str = cliente.birthDay or "N/A"
                
                meta_str = cliente.insight.indice if cliente.insight else "N/A"

                print(
                    f"{i+1:<3} "
                    f"{cliente.name:<25} "
                    f"{cliente.contact:<20} "
                    f"{birthday_str:<12} "
                    f"{cliente.accumulatedIndice:<8} "
                    f"{meta_str}"
                )
        
        print("\n===========================================================")
        input("Pressione Enter para continuar...")

    def exibir_status_insight(self, cliente: Client):
        self.limpar_tela()
        print(f"====== STATUS DE {cliente.name.upper()} ======\n")
        print(f"Pontos Acumulados: {cliente.accumulatedIndice}")
        if cliente.insight:
            print(f"Meta para Insight: {cliente.insight.indice} pontos")
            print(f"Recomendação: '{cliente.insight.recommendation}'")
            if cliente.can_redeem():
                print("\nStatus: PODE RESGATAR!")
            else:
                pontos_faltantes = cliente.insight.indice - cliente.accumulatedIndice
                print(f"\nStatus: Faltam {pontos_faltantes} ponto(s) para resgatar.")
        else:
            print("Nenhum insight configurado para este cliente.")
        print("\n" + "=" * 50)
        input("Pressione Enter para continuar...")

    def confirmar_resgate(self, cliente: Client) -> bool:
        self.limpar_tela()
        print("====== CONFIRMAR RESGATE ======\n")
        print(f"Cliente: {cliente.name}")
        print(f"Pontos Atuais: {cliente.accumulatedIndice}")
        print(f"Custo do Insight: {cliente.insight.indice} pontos")
        print(f"Saldo Após Resgate: {cliente.accumulatedIndice - cliente.insight.indice} pontos\n")
        confirmacao = input("Confirmar o resgate? (s/n): ").lower()
        return confirmacao == 's'

    def obter_escolha_cliente(self, clientes: list[Client], acao: str) -> Client | None:
        self.limpar_tela()
        print(f"====== SELECIONE UM CLIENTE PARA {acao.upper()} ======\n")
        if not clientes:
            self.exibir_mensagem("Nenhum cliente para selecionar.", sucesso=False)
            return None

        for i, cliente in enumerate(clientes):
            print(f"  {i + 1}. {cliente.name}")
        print("\n  0. Cancelar")

        while True:
            try:
                escolha = int(input("\nDigite o número do cliente: "))
                if 0 <= escolha <= len(clientes):
                    return None if escolha == 0 else clientes[escolha - 1]
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
    
    def obter_novos_dados_para_atualizar(self, cliente_antigo: Client) -> dict:
        self.limpar_tela()
        print(f"====== ATUALIZANDO '{cliente_antigo.name}' ======\n")
        print("Pressione Enter para manter o valor atual.")
        
        name = input(f"Novo nome ({cliente_antigo.name}): ")
        contact = input(f"Novo contato ({cliente_antigo.contact}): ")
        birthDay = input(f"Nova data de nascimento ({cliente_antigo.birthDay or 'N/A'}): ")

        print("\n--- Atualizar Dados do Insight ---")
        indice = input(f"Nova meta de índice ({cliente_antigo.insight.indice}): ")
        recommendation = input(f"Nova recomendação ({cliente_antigo.insight.recommendation}): ")

        return {
            "name": name.strip() or cliente_antigo.name,
            "contact": contact.strip() or cliente_antigo.contact,
            "birthDay": birthDay.strip() or cliente_antigo.birthDay,
            "indice": indice.strip() or cliente_antigo.insight.indice,
            "recommendation": recommendation.strip() or cliente_antigo.insight.recommendation
        }

    def confirmar_exclusao(self, nome: str) -> bool:
        self.limpar_tela()
        confirmacao = input(f"Tem certeza que deseja deletar o cliente '{nome}'? (s/n): ").lower()
        return confirmacao == 's'
    
    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")