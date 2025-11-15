import FreeSimpleGUI as sg
from models.specialty import Specialty

class EspecialityView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu_especialidades(self) -> str:
        """Exibe o menu principal de gerenciamento de Especialidades."""
        layout = [
            [sg.Text("GERENCIAR ESPECIALIDADES", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Listar todas as especialidades", key='1', size=(30, 2))],
            [sg.Button("Adicionar nova especialidade", key='2', size=(30, 2))],
            [sg.Button("Atualizar uma especialidade", key='3', size=(30, 2))],
            [sg.Button("Deletar uma especialidade", key='4', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]
        
        window = sg.Window("Gerenciar Especialidades", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
        return event

    def obter_dados_especialidade(self) -> dict | None:
        """Abre um formulário para adicionar uma nova especialidade."""
        layout = [
            [sg.Text("ADICIONAR NOVA ESPECIALIDADE", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(10,1)), sg.InputText(key='nome')],
            [sg.Text("Descrição:", size=(10,1)), sg.InputText(key='descricao')],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Nova Especialidade", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None 
            
            if event == "Salvar":
                if not values['nome'].strip():
                    sg.popup_error("O nome é obrigatório!")
                    continue
                window.close()
                return values

    def exibir_lista_especialidades(self, especialidades: list[Specialty]):
        """Exibe uma janela com uma tabela de todas as especialidades."""
        if not especialidades:
            sg.popup("Nenhuma especialidade cadastrada.")
            return

        dados_tabela = []
        for esp in especialidades:
            desc_curta = (esp.description[:40] + '...') if len(esp.description) > 40 else esp.description
            dados_tabela.append([esp.name, desc_curta])

        cabecalho = ["Nome", "Descrição"]
        
        layout = [
            [sg.Text("LISTA DE ESPECIALIDADES", font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[25, 40],
                      justification='left', num_rows=15, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window("Especialidades", layout)
        window.read()
        window.close()

    def obter_escolha_especialidade(self, especialidades: list[Specialty], acao: str) -> Specialty | None:
        """Abre uma janela para o usuário selecionar uma especialidade de uma lista."""
        if not especialidades:
            sg.popup_error(f"Nenhuma especialidade para {acao}.")
            return None
            
        nomes_especialidades = [esp.name for esp in especialidades]
        
        layout = [
            [sg.Text(f"Selecione uma especialidade para {acao}:")],
            [sg.Listbox(values=nomes_especialidades, size=(40, 10), key='-LIST-', enable_events=True)],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Selecionar Especialidade", layout)
        
        escolha = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Selecionar":
                if values['-LIST-']:
                    indice = window['-LIST-'].get_indexes()[0]
                    escolha = especialidades[indice] 
                    break
                else:
                    sg.popup_error("Por favor, selecione uma especialidade na lista.")
        
        window.close()
        return escolha

    def obter_novos_dados_para_atualizar(self, esp_antiga: Specialty) -> dict | None:
        """Abre um formulário pré-preenchido para atualizar uma especialidade."""
        layout = [
            [sg.Text(f"ATUALIZANDO: {esp_antiga.name}", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(10,1)), sg.InputText(esp_antiga.name, key='nome')],
            [sg.Text("Descrição:", size=(10,1)), sg.InputText(esp_antiga.description, key='descricao')],
            [sg.Button("Salvar Alterações"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Atualizar Especialidade", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if event == "Salvar Alterações":
                if not values['nome'].strip():
                    sg.popup_error("O nome não pode ficar vazio!")
                    continue
                
                window.close()
                return {
                    "nome": values['nome'].strip() if values['nome'].strip() else esp_antiga.name,
                    "descricao": values['descricao'].strip() if values['descricao'].strip() else esp_antiga.description
                }

    def confirmar_exclusao(self, nome_esp: str) -> bool:
        """Exibe um popup de confirmação Yes/No."""
        resposta = sg.popup_yes_no(f"Tem certeza que deseja DELETAR a especialidade '{nome_esp}'?\nEssa ação não pode ser desfeita.", title="Confirmar Exclusão")
        return resposta == "Yes"
        
    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe um popup de mensagem simples."""
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo, keep_on_top=True)
        else:
            sg.popup(msg, title=titulo, keep_on_top=True)