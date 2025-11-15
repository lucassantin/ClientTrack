from views.authentication_mod_view.employee_view import EmployeeView
from DAO.employee_dao import EmployeeSqliteDAO
from DAO.specialty_dao import SpecialtySqliteDAO
from models.employee import Employee

class EmployeeController:
    """Controller para o CRUD de Funcionários."""
    def __init__(self):
        self.view = EmployeeView()
        self.employee_dao = EmployeeSqliteDAO()
        self.specialty_dao = SpecialtySqliteDAO()

    def iniciar(self):
        """Inicia o loop do menu de gerenciamento de funcionários."""
        while True:
            opcao = self.view.exibir_menu_employees()
            match opcao:
                case '1': self._listar()
                case '2': self._adicionar()
                case '3': self._atualizar()
                case '4': self._deletar()
                case '0': break
                case _: self.view.exibir_mensagem("Opção inválida.", sucesso=False)

    def _listar(self):
        funcionarios = self.employee_dao.find_all()
        self.view.exibir_lista_employees(funcionarios)

    def _adicionar(self):
        especialidades = self.specialty_dao.find_all()
        if not especialidades:
            self.view.exibir_mensagem("É necessário ter ao menos uma especialidade cadastrada para adicionar um funcionário.", sucesso=False)
            return
            
        dados = self.view.obter_dados_employee(especialidades)
        if not dados:
            return

        try:
            novo_funcionario = Employee(
                name=dados['name'],
                contact=dados['contact'],
                specialty=dados['specialty'] 
            )
            self.employee_dao.create(novo_funcionario)
            self.view.exibir_mensagem("Funcionário adicionado com sucesso!")
        except (TypeError, ValueError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível adicionar funcionário: {e}", sucesso=False)

    def _atualizar(self):
        funcionarios = self.employee_dao.find_all()
        funcionario_selecionado = self.view.obter_escolha_employee(funcionarios, "atualizar")
        if not funcionario_selecionado:
            return

        especialidades = self.specialty_dao.find_all()
        novos_dados = self.view.obter_novos_dados_para_atualizar(funcionario_selecionado, especialidades) 
        if not novos_dados:
            return

        try:
            funcionario_selecionado.name = novos_dados['name']
            funcionario_selecionado.contact = novos_dados['contact']
            funcionario_selecionado.specialty = novos_dados['specialty']
            
            self.employee_dao.update(funcionario_selecionado)
            self.view.exibir_mensagem("Funcionário atualizado com sucesso!")
        except (TypeError, ValueError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível atualizar: {e}", sucesso=False)

    def _deletar(self):
        funcionarios = self.employee_dao.find_all()
        if not funcionarios:
            self.view.exibir_mensagem("Nenhum funcionário para deletar.", sucesso=False)
            return

        funcionario_selecionado = self.view.obter_escolha_employee(funcionarios, "deletar")
        if not funcionario_selecionado:
            return

        if self.view.confirmar_exclusao(funcionario_selecionado.name):
            try: 
                if self.employee_dao.delete(funcionario_selecionado.id):
                    self.view.exibir_mensagem("Funcionário deletado com sucesso!")
                else:
                    self.view.exibir_mensagem("Erro: Funcionário não encontrado para deletar.", sucesso=False)
            except Exception as e:
                self.view.exibir_mensagem(f"Não foi possível deletar: {e}", sucesso=False)