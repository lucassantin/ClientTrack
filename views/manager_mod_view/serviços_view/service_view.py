import os
from models.service import Service
from models.specialty import Specialty

class ServiceView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_servicos(self) -> str:
        """Exibe o menu de opções para gerenciar serviços."""
        self.limpar_tela()
        print("========== GERENCIAR SERVIÇOS ==========\n")
        print("  1. Listar todos os serviços")
        print("  2. Adicionar novo serviço")
        print("  3. Atualizar um serviço")
        print("  4. Deletar um serviço")
        print("\n  0. Voltar ao menu anterior")
        print("\n========================================")
        return input("Escolha uma opção: ")

    def obter_dados_servico(self) -> dict:
        """Coleta do usuário os dados para um novo serviço."""
        self.limpar_tela()
        print("====== ADICIONAR NOVO SERVIÇO ======\n")
        print("(Deixe um campo em branco para cancelar)\n")
        nome = input("Nome do serviço: ")
        if not nome: return {} 
        
        descricao = input("Descrição do serviço: ")
        if not descricao: return {}

        preco = input("Preço do serviço (ex: 150.00): ")
        if not preco: return {}
        
        return {"nome": nome, "descricao": descricao, "preco": preco}

    def exibir_lista_servicos(self, servicos: list):
        """Mostra uma lista formatada de serviços."""
        self.limpar_tela()
        print("=========== LISTA DE SERVIÇOS ===========\n")
        if not servicos:
            print("Nenhum serviço cadastrado.")
        else:
            print(f"{'#':<3} {'NOME':<30} {'PREÇO (R$)'}")
            print("-" * 45)
            for i, servico in enumerate(servicos):
                preco_formatado = f"{servico.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                print(f"{i+1:<3} {servico.name:<30} {preco_formatado}")
        
        print("\n=========================================")
        input("Pressione Enter para continuar...")
        
    def obter_escolha_servico(self, servicos: list, acao: str):
        """Pede ao usuário para escolher um serviço da lista."""
        self.limpar_tela()
        print(f"====== SELECIONE UM SERVIÇO PARA {acao.upper()} ======\n")
        if not servicos:
            return None
            
        for i, servico in enumerate(servicos):
            print(f"  {i + 1}. {servico.name}")
        print("\n  0. Cancelar")

        while True:
            try:
                escolha = int(input("Digite o número do serviço: "))
                if 0 <= escolha <= len(servicos):
                    return None if escolha == 0 else servicos[escolha - 1]
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe uma mensagem de feedback."""
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")

    def obter_novos_dados_para_atualizar(self, servico_antigo: 'Service') -> dict:
        """Pede os novos dados para um serviço que está sendo atualizado."""
        self.limpar_tela()
        print(f"====== ATUALIZANDO O SERVIÇO '{servico_antigo.name}' ======\n")
        print("Digite os novos dados. Pressione Enter para manter o valor atual.")
        print("(Deixe o nome em branco para cancelar a operação)\n")

        nome = input(f"Novo nome ({servico_antigo.name}): ")
        if nome == "": 
            return {} 

        descricao = input(f"Nova descrição ({servico_antigo.description}): ")
        preco = input(f"Novo preço ({servico_antigo.price:.2f}): ")
        
        return {
            "nome": nome if nome.strip() else servico_antigo.name,
            "descricao": descricao if descricao.strip() else servico_antigo.description,
            "preco": preco if preco.strip() else servico_antigo.price
        }

    def confirmar_exclusao(self, nome_servico: str) -> bool:
        """Pede confirmação do usuário antes de deletar."""
        self.limpar_tela()
        print(f"====== CONFIRMAR EXCLUSÃO ======\n")
        print(f"ATENÇÃO: Esta ação é irreversível.")
        confirmacao = input(f"Tem certeza que deseja deletar o serviço '{nome_servico}'? (s/n): ").lower()
        return confirmacao == 's'


    def exibir_lista_servicos(self, servicos: list):
        self.limpar_tela()
        print("======================== LISTA DE SERVIÇOS ========================\n")
        if not servicos:
            print("Nenhum serviço cadastrado.")
        else:
            print(f"{'#':<3} {'NOME':<30} {'ESPECIALIDADE':<20} {'PREÇO (R$)'}")
            print("-" * 75)
            for i, servico in enumerate(servicos):
                especialidade_nome = servico.specialty.name if servico.specialty else "N/A"
                preco_formatado = f"{servico.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                print(f"{i+1:<3} {servico.name:<30} {especialidade_nome:<20} {preco_formatado}")
        
        print("\n===================================================================")
        input("Pressione Enter para continuar...")
        
    def obter_dados_servico(self, especialidades: list[Specialty]) -> dict | None:
        """Coleta do usuário os dados para um novo serviço, incluindo a especialidade."""
        self.limpar_tela()
        print("====== ADICIONAR NOVO SERVIÇO ======\n")
        
        nome = input("Nome do serviço: ")
        if not nome.strip(): return None
        
        descricao = input("Descrição do serviço: ")
        preco = input("Preço do serviço (ex: 150.00): ")
        if not preco.strip(): return None

        print("\n--- Associar a uma Especialidade (opcional) ---")
        for i, esp in enumerate(especialidades):
            print(f"  {i + 1}. {esp.name}")
        print("  0. Nenhuma / Deixar em branco")

        especialidade_selecionada = None
        while True:
            try:
                escolha_str = input("\nEscolha a especialidade: ")
                if not escolha_str: 
                    break
                
                escolha = int(escolha_str)
                if escolha == 0:
                    break
                elif 1 <= escolha <= len(especialidades):
                    especialidade_selecionada = especialidades[escolha - 1]
                    break
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        
        return {
            "nome": nome, 
            "descricao": descricao, 
            "preco": preco,
            "specialty": especialidade_selecionada 
        }