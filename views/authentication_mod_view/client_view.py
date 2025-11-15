import FreeSimpleGUI as sg
from models.client import Client

class ClientView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu_clientes(self) -> str:
        layout = [
            [sg.Text("GERENCIAR CLIENTES E FIDELIDADE", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Listar todos os clientes", key='1', size=(30, 2))],
            [sg.Button("Adicionar novo cliente", key='2', size=(30, 2))],
            [sg.Button("Atualizar um cliente", key='3', size=(30, 2))],
            [sg.Button("Deletar um cliente", key='4', size=(30, 2))],
            [sg.HorizontalSeparator()],
            [sg.Button("Verificar Pontuação/Insight", key='5', size=(30, 2))],
            [sg.Button("Resgatar Insight", key='6', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]
        
        window = sg.Window("Gerenciar Clientes", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
        return event

    def obter_dados_cliente(self) -> dict | None:
        layout = [
            [sg.Text("ADICIONAR NOVO CLIENTE", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(20,1)), sg.InputText(key='name')],
            [sg.Text("Contato:", size=(20,1)), sg.InputText(key='contact')],
            [sg.Text("Data Nasc(AAAA-MM-DD):", size=(20,1)), sg.InputText(key='birthDay', tooltip="Formato: AAAA-MM-DD")],
            [sg.HorizontalSeparator()],
            [sg.Text("Dados para o Insight (Fidelidade):")],
            [sg.Text("Meta (Pontos):", size=(20,1)), sg.InputText(key='indice')],
            [sg.Text("Recomendação:", size=(20,1)), sg.InputText(key='recommendation')],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Novo Cliente", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            
            if event == "Salvar":
                if not values['name'].strip():
                    sg.popup_error("O nome é obrigatório!")
                    continue
                window.close()
                return values

    def exibir_lista_clientes(self, clientes: list[Client]):
        if not clientes:
            sg.popup("Nenhum cliente cadastrado.")
            return

        dados_tabela = []
        for c in clientes:
            nasc = c.birthDay if c.birthDay else "N/A"
            meta = c.insight.indice if c.insight else "N/A"
            dados_tabela.append([c.name, c.contact, nasc, c.accumulatedIndice, meta])

        cabecalho = ["Nome", "Contato", "Nascimento", "Pontos", "Meta"]
        
        layout = [
            [sg.Text("LISTA DE CLIENTES", font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[20, 15, 12, 8, 8],
                      justification='left', num_rows=15, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window("Lista de Clientes", layout)
        window.read()
        window.close()

    def obter_escolha_cliente(self, clientes: list[Client], acao: str) -> Client | None:
        if not clientes:
            sg.popup_error("Nenhum cliente para selecionar.")
            return None
            
        nomes_clientes = [f"{c.name} (Pontos: {c.accumulatedIndice})" for c in clientes]
        
        layout = [
            [sg.Text(f"Selecione um cliente para {acao}:")],
            [sg.Listbox(values=nomes_clientes, size=(40, 10), key='-LIST-', enable_events=True)],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Selecionar Cliente", layout)
        
        escolha = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Selecionar":
                if values['-LIST-']:
                    indice = window['-LIST-'].get_indexes()[0]
                    escolha = clientes[indice]
                    break
                else:
                    sg.popup_error("Por favor, selecione um cliente na lista.")
        
        window.close()
        return escolha

    def obter_novos_dados_para_atualizar(self, cliente_antigo: Client) -> dict | None:
        layout = [
            [sg.Text(f"ATUALIZAR: {cliente_antigo.name}", font=("Helvetica", 14))],
            [sg.Text("Nome:", size=(15,1)), sg.InputText(cliente_antigo.name, key='name')],
            [sg.Text("Contato:", size=(15,1)), sg.InputText(cliente_antigo.contact, key='contact')],
            [sg.Text("Data Nasc.:", size=(15,1)), sg.InputText(cliente_antigo.birthDay or "", key='birthDay')],
            [sg.HorizontalSeparator()],
            [sg.Text("Dados do Insight:")],
            [sg.Text("Meta (Pontos):", size=(15,1)), sg.InputText(str(cliente_antigo.insight.indice), key='indice')],
            [sg.Text("Recomendação:", size=(15,1)), sg.InputText(cliente_antigo.insight.recommendation, key='recommendation')],
            [sg.Button("Salvar Alterações"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Atualizar Cliente", layout)
        
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                window.close()
                return None
            if event == "Salvar Alterações":
                if not values['name'].strip():
                    sg.popup_error("O nome não pode ficar vazio!")
                    continue
                window.close()
                return values

    def exibir_status_insight(self, cliente: Client):
        msg = f"Cliente: {cliente.name}\n"
        msg += f"Pontos Acumulados: {cliente.accumulatedIndice}\n\n"
        
        if cliente.insight:
            msg += f"Meta: {cliente.insight.indice} pontos\n"
            msg += f"Prêmio: {cliente.insight.recommendation}\n"
            
            if cliente.can_redeem():
                msg += "\nSTATUS: PODE RESGATAR! 🎉"
            else:
                faltam = cliente.insight.indice - cliente.accumulatedIndice
                msg += f"\nSTATUS: Faltam {faltam} pontos."
        else:
            msg += "Este cliente não tem insight configurado."
            
        sg.popup(msg, title=f"Status de {cliente.name}")

    def confirmar_resgate(self, cliente: Client) -> bool:
        msg = f"Confirmar resgate para {cliente.name}?\n\n"
        msg += f"Pontos atuais: {cliente.accumulatedIndice}\n"
        msg += f"Custo: {cliente.insight.indice}\n"
        msg += f"Saldo final: {cliente.accumulatedIndice - cliente.insight.indice}"
        
        resposta = sg.popup_yes_no(msg, title="Confirmar Resgate")
        return resposta == "Yes"

    def confirmar_exclusao(self, nome: str) -> bool:
        resposta = sg.popup_yes_no(f"Tem certeza que deseja DELETAR o cliente '{nome}'?\nEssa ação não pode ser desfeita.", title="Confirmar Exclusão")
        return resposta == "Yes"

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo)
        else:
            sg.popup(msg, title=titulo)