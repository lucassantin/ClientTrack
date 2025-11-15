import FreeSimpleGUI as sg
from models.payment_type import PaymentType

class PaymentView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu_gerenciamento(self) -> str:
        """Exibe o menu principal de gerenciamento de Tipos de Pagamento."""
        layout = [
            [sg.Text("GERENCIAR TIPOS DE PAGAMENTO", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Listar todos os tipos", key='1', size=(30, 2))],
            [sg.Button("Adicionar novo tipo", key='2', size=(30, 2))],
            [sg.Button("Atualizar um tipo existente", key='3', size=(30, 2))],
            [sg.Button("Deletar um tipo", key='4', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]
        
        window = sg.Window("Gerenciar Tipos de Pagamento", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
        return event

    def obter_dados_tipo_pagamento(self) -> dict | None:
        """Abre um popup para o usuário digitar o nome do novo tipo."""
        nome = sg.popup_get_text(
            "Digite o nome do novo tipo de pagamento (ex: Pix, Dinheiro):", 
            title="Adicionar Novo Tipo"
        )
        
        if nome is None: 
            return None
        
        return {"nome": nome}

    def exibir_lista_tipos_pagamento(self, tipos: list[PaymentType]):
        """Exibe uma janela com uma tabela de todos os tipos de pagamento."""
        if not tipos:
            sg.popup("Nenhum tipo de pagamento cadastrado.")
            return

        dados_tabela = [[tipo.name, tipo.id] for tipo in tipos]
        cabecalho = ["Nome", "ID do Banco de Dados"]
        
        layout = [
            [sg.Text("LISTA DE TIPOS DE PAGAMENTO", font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[25, 35],
                      justification='left', num_rows=10, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window("Tipos de Pagamento", layout)
        window.read()
        window.close()

    def obter_escolha_tipo(self, tipos: list[PaymentType], acao: str) -> PaymentType | None:
        """Abre uma janela para o usuário selecionar um tipo de pagamento de uma lista."""
        if not tipos:
            sg.popup_error(f"Nenhum tipo de pagamento para {acao}.")
            return None
            
        nomes_tipos = [tipo.name for tipo in tipos]
        
        layout = [
            [sg.Text(f"Selecione um tipo de pagamento para {acao}:")],
            [sg.Listbox(values=nomes_tipos, size=(40, 10), key='-LIST-', enable_events=True)],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Selecionar Tipo de Pagamento", layout)
        
        escolha = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Selecionar":
                if values['-LIST-']:
                    indice = window['-LIST-'].get_indexes()[0]
                    escolha = tipos[indice] 
                    break
                else:
                    sg.popup_error("Por favor, selecione um tipo na lista.")
        
        window.close()
        return escolha

    def obter_novos_dados_para_atualizar(self, tipo_antigo: PaymentType) -> dict | None:
        """Abre um popup para editar o nome de um tipo de pagamento."""
        novo_nome = sg.popup_get_text(
            f"Digite o novo nome para '{tipo_antigo.name}':",
            title="Atualizar Tipo de Pagamento",
            default_text=tipo_antigo.name
        )
        
        if novo_nome is None:
            return None
            
        return {"nome": novo_nome}

    def confirmar_exclusao(self, nome_tipo: str) -> bool:
        """Exibe um popup de confirmação Yes/No."""
        resposta = sg.popup_yes_no(f"Tem certeza que deseja DELETAR o tipo '{nome_tipo}'?\nEssa ação não pode ser desfeita.", title="Confirmar Exclusão")
        return resposta == "Yes"

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe um popup de mensagem simples."""
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo, keep_on_top=True)
        else:
            sg.popup(msg, title=titulo, keep_on_top=True)