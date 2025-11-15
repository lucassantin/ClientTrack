import FreeSimpleGUI as sg
from models.service import Service
from models.specialty import Specialty

class ServiceView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu_servicos(self) -> str:
        """Exibe o menu principal de gerenciamento de Serviços."""
        layout = [
            [sg.Text("GERENCIAR SERVIÇOS", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Listar todos os serviços", key='1', size=(30, 2))],
            [sg.Button("Adicionar novo serviço", key='2', size=(30, 2))],
            [sg.Button("Atualizar um serviço", key='3', size=(30, 2))],
            [sg.Button("Deletar um serviço", key='4', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]
        
        window = sg.Window("Gerenciar Serviços", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
        return event

    def obter_dados_servico(self, especialidades: list[Specialty]) -> dict | None:
        """Abre um formulário para adicionar um novo serviço."""
        
        nomes_especialidades = ["Nenhuma"] + [esp.name for esp in especialidades]
        
        layout = [
            [sg.Text("ADICIONAR NOVO SERVIÇO", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(15,1)), sg.InputText(key='nome')],
            [sg.Text("Descrição:", size=(15,1)), sg.InputText(key='descricao')],
            [sg.Text("Preço (ex: 99.50):", size=(15,1)), sg.InputText(key='preco')],
            [sg.HorizontalSeparator()],
            [sg.Text("Especialidade:", size=(15,1)), 
             sg.Combo(nomes_especialidades, default_value=nomes_especialidades[0], key='specialty_name', readonly=True, size=(25, 1))],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Novo Serviço", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if event == "Salvar":
                if not values['nome'].strip():
                    sg.popup_error("O nome é obrigatório!")
                    continue
                if not values['preco'].strip():
                    sg.popup_error("O preço é obrigatório!")
                    continue
                
                specialty_obj = None
                if values['specialty_name'] != "Nenhuma":
                    for esp in especialidades:
                        if esp.name == values['specialty_name']:
                            specialty_obj = esp
                            break
                
                window.close()
                return {
                    "nome": values['nome'], 
                    "descricao": values['descricao'], 
                    "preco": values['preco'],
                    "especialidade": specialty_obj 
                }

    def exibir_lista_servicos(self, servicos: list[Service]):
        """Exibe uma tabela com todos os serviços."""
        if not servicos:
            sg.popup("Nenhum serviço cadastrado.")
            return

        dados_tabela = []
        for servico in servicos:
            especialidade_nome = servico.specialty.name if servico.specialty else "N/A"
            preco_formatado = f"R$ {servico.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            dados_tabela.append([servico.name, especialidade_nome, preco_formatado])

        cabecalho = ["Nome", "Especialidade", "Preço"]
        
        layout = [
            [sg.Text("LISTA DE SERVIÇOS", font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[25, 20, 15],
                      justification='left', num_rows=15, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window("Lista de Serviços", layout)
        window.read()
        window.close()

    def obter_escolha_servico(self, servicos: list[Service], acao: str) -> Service | None:
        """Abre uma janela para o usuário selecionar um serviço de uma lista."""
        if not servicos:
            sg.popup_error(f"Nenhum serviço para {acao}.")
            return None
            
        nomes_servicos = [f"{s.name} (R$ {s.price:.2f})" for s in servicos]
        
        layout = [
            [sg.Text(f"Selecione um serviço para {acao}:")],
            [sg.Listbox(values=nomes_servicos, size=(40, 10), key='-LIST-', enable_events=True)],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Selecionar Serviço", layout)
        
        escolha = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Selecionar":
                if values['-LIST-']:
                    indice = window['-LIST-'].get_indexes()[0]
                    escolha = servicos[indice]
                    break
                else:
                    sg.popup_error("Por favor, selecione um serviço na lista.")
        
        window.close()
        return escolha

    def obter_novos_dados_para_atualizar(self, servico_antigo: Service, especialidades_disponiveis: list[Specialty]) -> dict | None:
        """Abre um formulário pré-preenchido para atualizar um serviço."""
        
        nomes_especialidades = ["Nenhuma"] + [esp.name for esp in especialidades_disponiveis]
        
        default_specialty_name = "Nenhuma"
        if servico_antigo.specialty:
            default_specialty_name = servico_antigo.specialty.name
        
        layout = [
            [sg.Text(f"ATUALIZAR: {servico_antigo.name}", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(15,1)), sg.InputText(servico_antigo.name, key='nome')],
            [sg.Text("Descrição:", size=(15,1)), sg.InputText(servico_antigo.description, key='descricao')],
            [sg.Text("Preço:", size=(15,1)), sg.InputText(f"{servico_antigo.price:.2f}", key='preco')],
            [sg.HorizontalSeparator()],
            [sg.Text("Especialidade:", size=(15,1)), 
             sg.Combo(nomes_especialidades, default_value=default_specialty_name, key='specialty_name', readonly=True, size=(25, 1))],
            [sg.Button("Salvar Alterações"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Atualizar Serviço", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if event == "Salvar Alterações":
                if not values['nome'].strip():
                    sg.popup_error("O nome não pode ficar vazio!")
                    continue
                if not values['preco'].strip():
                    sg.popup_error("O preço não pode ficar vazio!")
                    continue
                
                specialty_obj = None
                if values['specialty_name'] != "Nenhuma":
                    for esp in especialidades_disponiveis:
                        if esp.name == values['specialty_name']:
                            specialty_obj = esp
                            break
                            
                window.close()
                return {
                    "nome": values['nome'], 
                    "descricao": values['descricao'], 
                    "preco": values['preco'],
                    "especialidade": specialty_obj 
                }

    def confirmar_exclusao(self, nome_servico: str) -> bool:
        """Exibe um popup de confirmação Yes/No para exclusão."""
        resposta = sg.popup_yes_no(f"Tem certeza que deseja DELETAR o serviço '{nome_servico}'?\nEssa ação não pode ser desfeita.", title="Confirmar Exclusão")
        return resposta == "Yes"

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe um popup de mensagem simples."""
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo, keep_on_top=True)
        else:
            sg.popup(msg, title=titulo, keep_on_top=True)