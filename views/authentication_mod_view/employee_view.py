import os
from models.employee import Employee
from models.specialty import Specialty

class EmployeeView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_employees(self) -> str:
        self.limpar_tela()
        print("====== GERENCIAR FUNCIONÁRIOS ======\n")
        print("  1. Listar todos os funcionários")
        print("  2. Adicionar novo funcionário")
        print("  3. Atualizar um funcionário")
        print("  4. Deletar um funcionário")
        print("\n  0. Voltar")
        print("\n==================================")
        return input("Escolha uma opção: ")

    def obter_dados_employee(self, especialidades: list[Specialty]) -> dict:
        self.limpar_tela()
        print("====== ADICIONAR NOVO FUNCIONÁRIO ======\n")
        name = input("Nome: ")
        if not name.strip(): return {}
        
        contact = input("Contato (Telefone/Email): ")
        
        print("\n--- Associar Especialidade ---")
        for i, esp in enumerate(especialidades):
            print(f"  {i + 1}. {esp.name}")
        print("  0. Nenhuma")

        especialidade_selecionada = None
        while True:
            try:
                escolha = int(input("Escolha a especialidade: "))
                if escolha == 0:
                    break
                elif 1 <= escolha <= len(especialidades):
                    especialidade_selecionada = especialidades[escolha - 1]
                    break
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

        return {"name": name, "contact": contact, "specialty": especialidade_selecionada}

    def exibir_lista_employees(self, employees: list[Employee]):
        self.limpar_tela()
        print("================= LISTA DE FUNCIONÁRIOS =================\n")
        if not employees:
            print("Nenhum funcionário cadastrado.")
        else:
            print(f"{'#':<3} {'NOME':<30} {'CONTATO':<20} {'ESPECIALIDADE'}")
            print("-" * 75)
            for i, emp in enumerate(employees):
                specialty_name = emp.specialty.name if emp.specialty else "N/A"
                print(f"{i+1:<3} {emp.name:<30} {emp.contact:<20} {specialty_name}")
        
        print("\n=======================================================")
        input("Pressione Enter para continuar...")

    def obter_escolha_employee(self, employees: list[Employee], acao: str) -> Employee | None:
        self.limpar_tela()
        print(f"====== SELECIONE UM FUNCIONÁRIO PARA {acao.upper()} ======\n")
        if not employees:
            self.exibir_mensagem("Nenhum funcionário para selecionar.", sucesso=False)
            return None

        for i, emp in enumerate(employees):
            print(f"  {i + 1}. {emp.name}")
        print("\n  0. Cancelar")

        while True:
            try:
                escolha = int(input("\nDigite o número do funcionário: "))
                if 0 <= escolha <= len(employees):
                    return None if escolha == 0 else employees[escolha - 1]
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    def obter_novos_dados_para_atualizar(self, employee: Employee, especialidades: list[Specialty]) -> dict:
        self.limpar_tela()
        print(f"====== ATUALIZANDO '{employee.name}' ======\n")
        
        name = input(f"Novo nome ({employee.name}): ")
        contact = input(f"Novo contato ({employee.contact}): ")
        
        print("\n--- Alterar Especialidade ---")
        current_specialty = employee.specialty.name if employee.specialty else "Nenhuma"
        print(f"Especialidade Atual: {current_specialty}\n")
        
        for i, esp in enumerate(especialidades):
            print(f"  {i + 1}. {esp.name}")
        print("\n  0. Remover especialidade")
        print("  [Enter]. Manter especialidade atual")

        nova_especialidade = employee.specialty
        while True:
            escolha_str = input("Escolha a nova especialidade: ")
            if not escolha_str: break
            try:
                escolha = int(escolha_str)
                if escolha == 0:
                    nova_especialidade = None
                    break
                elif 1 <= escolha <= len(especialidades):
                    nova_especialidade = especialidades[escolha - 1]
                    break
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida.")
        
        return {
            "name": name.strip() or employee.name,
            "contact": contact.strip() or employee.contact,
            "specialty": nova_especialidade
        }

    def confirmar_exclusao(self, nome: str) -> bool:
        self.limpar_tela()
        confirmacao = input(f"Tem certeza que deseja deletar o funcionário '{nome}'? (s/n): ").lower()
        return confirmacao == 's'

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")