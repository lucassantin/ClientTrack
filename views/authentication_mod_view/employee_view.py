import FreeSimpleGUI as sg
from models.employee import Employee
from models.specialty import Specialty

class EmployeeView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu_employees(self) -> str:
        """Exibe o menu principal de gerenciamento de funcionários."""
        layout = [
            [sg.Text("GERENCIAR FUNCIONÁRIOS", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Listar todos os funcionários", key='1', size=(30, 2))],
            [sg.Button("Adicionar novo funcionário", key='2', size=(30, 2))],
            [sg.Button("Atualizar um funcionário", key='3', size=(30, 2))],
            [sg.Button("Deletar um funcionário", key='4', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]
        
        window = sg.Window("Gerenciar Funcionários", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
        return event

    def obter_dados_employee(self, especialidades: list[Specialty]) -> dict | None:
        """Abre um formulário para adicionar um novo funcionário."""
        
        nomes_especialidades = ["Nenhuma"] + [esp.name for esp in especialidades]
        
        layout = [
            [sg.Text("ADICIONAR NOVO FUNCIONÁRIO", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(15,1)), sg.InputText(key='name')],
            [sg.Text("Contato:", size=(15,1)), sg.InputText(key='contact')],
            [sg.HorizontalSeparator()],
            [sg.Text("Associar Especialidade:", size=(15,1)), 
             sg.Combo(nomes_especialidades, default_value=nomes_especialidades[0], key='specialty_name', readonly=True, size=(25, 1))],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Novo Funcionário", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if event == "Salvar":
                if not values['name'].strip():
                    sg.popup_error("O nome é obrigatório!")
                    continue
                
                specialty_obj = None
                if values['specialty_name'] != "Nenhuma":
                    for esp in especialidades:
                        if esp.name == values['specialty_name']:
                            specialty_obj = esp
                            break
                
                window.close()
                return {
                    "name": values['name'], 
                    "contact": values['contact'], 
                    "specialty": specialty_obj 
                }

    def exibir_lista_employees(self, employees: list[Employee]):
        """Exibe uma tabela com todos os funcionários."""
        if not employees:
            sg.popup("Nenhum funcionário cadastrado.")
            return

        dados_tabela = []
        for emp in employees:
            specialty_name = emp.specialty.name if emp.specialty else "N/A"
            dados_tabela.append([emp.name, emp.contact, specialty_name])

        cabecalho = ["Nome", "Contato", "Especialidade"]
        
        layout = [
            [sg.Text("LISTA DE FUNCIONÁRIOS", font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[25, 20, 20],
                      justification='left', num_rows=15, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window("Lista de Funcionários", layout)
        window.read()
        window.close()

    def obter_escolha_employee(self, employees: list[Employee], acao: str) -> Employee | None:
        """Abre uma janela para o usuário selecionar um funcionário de uma lista."""
        if not employees:
            sg.popup_error(f"Nenhum funcionário para {acao}.")
            return None
            
        nomes_funcionarios = [f"{emp.name} ({emp.specialty.name if emp.specialty else 'Sem especialidade'})" for emp in employees]
        
        layout = [
            [sg.Text(f"Selecione um funcionário para {acao}:")],
            [sg.Listbox(values=nomes_funcionarios, size=(40, 10), key='-LIST-', enable_events=True)],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Selecionar Funcionário", layout)
        
        escolha = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Selecionar":
                if values['-LIST-']:
                    indice = window['-LIST-'].get_indexes()[0]
                    escolha = employees[indice]
                    break
                else:
                    sg.popup_error("Por favor, selecione um funcionário na lista.")
        
        window.close()
        return escolha

    def obter_novos_dados_para_atualizar(self, employee: Employee, especialidades: list[Specialty]) -> dict | None:
        """Abre um formulário pré-preenchido para atualizar um funcionário."""
        
        nomes_especialidades = ["Nenhuma"] + [esp.name for esp in especialidades]
        
        default_specialty_name = "Nenhuma"
        if employee.specialty:
            default_specialty_name = employee.specialty.name
        
        layout = [
            [sg.Text(f"ATUALIZAR: {employee.name}", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(15,1)), sg.InputText(employee.name, key='name')],
            [sg.Text("Contato:", size=(15,1)), sg.InputText(employee.contact, key='contact')],
            [sg.HorizontalSeparator()],
            [sg.Text("Especialidade:", size=(15,1)), 
             sg.Combo(nomes_especialidades, default_value=default_specialty_name, key='specialty_name', readonly=True, size=(25, 1))],
            [sg.Button("Salvar Alterações"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Atualizar Funcionário", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if event == "Salvar Alterações":
                if not values['name'].strip():
                    sg.popup_error("O nome não pode ficar vazio!")
                    continue
                
                specialty_obj = None
                if values['specialty_name'] != "Nenhuma":
                    for esp in especialidades:
                        if esp.name == values['specialty_name']:
                            specialty_obj = esp
                            break
                            
                window.close()
                return {
                    "name": values['name'], 
                    "contact": values['contact'], 
                    "specialty": specialty_obj 
                }

    def confirmar_exclusao(self, nome: str) -> bool:
        """Exibe um popup de confirmação Yes/No para exclusão."""
        resposta = sg.popup_yes_no(f"Tem certeza que deseja DELETAR o funcionário '{nome}'?\nEssa ação não pode ser desfeita.", title="Confirmar Exclusão")
        return resposta == "Yes"

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe um popup de mensagem."""
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo, keep_on_top=True)
        else:
            sg.popup(msg, title=titulo, keep_on_top=True)