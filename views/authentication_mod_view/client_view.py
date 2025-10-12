import os
from models.client import Client

class ClientView:
    def limpar_tela(self): ...# ...

    def exibir_menu_clientes(self) -> str:
        self.limpar_tela()
        print("======= GERENCIAR CLIENTES =======\n")
        print("  1. Listar todos os clientes")
        print("  2. Adicionar novo cliente")
        print("  3. Atualizar um cliente")
        print("  4. Deletar um cliente")
        print("\n  0. Voltar")
        print("\n================================")
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
        print("=========== LISTA DE CLIENTES ===========\n")
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            print(f"{'#':<3} {'NOME':<30} {'CONTATO':<20} {'ANIVERSÁRIO'}")
            print("-" * 75)
            for i, cliente in enumerate(clientes):
                print(f"{i+1:<3} {cliente.name:<30} {cliente.contact:<20} {cliente.birthday or 'N/A'}")
        
        print("\n=========================================")
        input("Pressione Enter para continuar...")

    def obter_escolha_cliente(self, clientes: list[Client], acao: str): ...# ... (similar a outras views)
    
    def obter_novos_dados_para_atualizar(self, cliente_antigo: Client) -> dict:
        print(f"====== ATUALIZANDO '{cliente_antigo.name}' ======\n")
        print("Pressione Enter para manter o valor atual.")
        
        name = input(f"Novo nome ({cliente_antigo.name}): ")
        contact = input(f"Novo contato ({cliente_antigo.contact}): ")
        birthDay = input(f"Nova data de nascimento ({cliente_antigo.birthday or 'N/A'}): ")

        return {
            "name": name or cliente_antigo.name,
            "contact": contact or cliente_antigo.contact,
            "birthDay": birthDay or cliente_antigo.birthday
        }

    def confirmar_exclusao(self, nome: str) -> bool: ...# ... (similar a outras views)
    
    def exibir_mensagem(self, msg: str, sucesso: bool = True): ...# ... (similar a outras views)