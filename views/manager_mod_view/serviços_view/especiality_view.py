import os
from models.specialty import Specialty

class EspecialityView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_especialidades(self) -> str:
        self.limpar_tela()
        print("======== GERENCIAR ESPECIALIDADES ========\n")
        print("  1. Listar todas as especialidades")
        print("  2. Adicionar nova especialidade")
        print("  3. Atualizar uma especialidade")
        print("  4. Deletar uma especialidade")
        print("\n  0. Voltar ao menu anterior")
        print("\n========================================")
        return input("Escolha uma opção: ")

    def obter_dados_especialidade(self) -> dict:
        self.limpar_tela()
        print("====== ADICIONAR NOVA ESPECIALIDADE ======\n")
        print("(Deixe o nome em branco para cancelar)\n")
        nome = input("Nome da especialidade: ")
        if not nome: 
            return {}
        
        descricao = input("Descrição da especialidade: ")
        
        return {"nome": nome, "descricao": descricao}

    def exibir_lista_especialidades(self, especialidades: list[Specialty]):
        self.limpar_tela()
        print("======== LISTA DE ESPECIALIDADES =========\n")
        if not especialidades:
            print("Nenhuma especialidade cadastrada.")
        else:
            print(f"{'#':<3} {'NOME':<30} {'DESCRIÇÃO'}")
            print("-" * 70)
            for i, esp in enumerate(especialidades):
                desc_curta = (esp.description[:35] + '...') if len(esp.description) > 35 else esp.description
                print(f"{i+1:<3} {esp.name:<30} {desc_curta}")
        
        print("\n==========================================")
        input("Pressione Enter para continuar...")

    def obter_escolha_especialidade(self, especialidades: list[Specialty], acao: str) -> Specialty | None:
        self.limpar_tela()
        print(f"====== SELECIONE UMA ESPECIALIDADE PARA {acao.upper()} ======\n")
        if not especialidades:
            print("Nenhuma especialidade para selecionar.")
            input("\nPressione Enter para voltar...")
            return None
            
        for i, esp in enumerate(especialidades):
            print(f"  {i + 1}. {esp.name}")
        print("\n  0. Cancelar")

        while True:
            try:
                escolha = int(input("Digite o número da especialidade: "))
                if 0 <= escolha <= len(especialidades):
                    return None if escolha == 0 else especialidades[escolha - 1]
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def obter_novos_dados_para_atualizar(self, esp_antiga: Specialty) -> dict:
        self.limpar_tela()
        print(f"====== ATUALIZANDO '{esp_antiga.name}' ======\n")
        print("Digite os novos dados. Pressione Enter para manter o valor atual.")
        
        nome = input(f"Novo nome ({esp_antiga.name}): ")
        descricao = input(f"Nova descrição ({esp_antiga.description}): ")
        
        return {
            "nome": nome if nome.strip() else esp_antiga.name,
            "descricao": descricao if descricao.strip() else esp_antiga.description
        }

    def confirmar_exclusao(self, nome_esp: str) -> bool:
        self.limpar_tela()
        confirmacao = input(f"Tem certeza que deseja deletar a especialidade '{nome_esp}'? (s/n): ").lower()
        return confirmacao == 's'
        
    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")