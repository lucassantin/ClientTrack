import FreeSimpleGUI as sg

class MainView:
    def __init__(self):
        """Define o tema padrão para todas as janelas desta view."""
        sg.theme('DarkBlue') 

    def exibir_menu(self) -> str:
        """
        Cria e exibe a janela do menu principal.
        Retorna a 'key' (chave) do botão que foi clicado.
        """
        
        layout_gerenciamento = [
            [sg.Button("Gerenciar Tipos de Pagamento", key='1', size=(30, 2))],
            [sg.Button("Gerenciar Serviços", key='2', size=(30, 2))],
            [sg.Button("Gerenciar Especialidades", key='3', size=(30, 2))],
            [sg.Button("Gerenciar Agendamentos", key='4', size=(30, 2))]
        ]
        
        layout_usuarios = [
            [sg.Button("Gerenciar Clientes", key='5', size=(30, 2))],
            [sg.Button("Gerenciar Funcionários", key='6', size=(30, 2))]
        ]

        layout_analise = [
            [sg.Button("Gerar Relatórios", key='7', size=(30, 2))]
        ]
        
        layout_principal = [
            [sg.Text("Bem-vindo ao TrackClients!", font=("Helvetica", 20), justification='c', pad=(10, 20))],
            [sg.Frame("Gerenciamento", layout_gerenciamento, element_justification='c')],
            [sg.Frame("Autenticação e Usuários", layout_usuarios, element_justification='c')],
            [sg.Frame("Análise", layout_analise, element_justification='c')],
            [sg.Button("Sair", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(10, 20))]
        ]

        # Cria a janela
        window = sg.Window(
            "TrackClients - Menu Principal", 
            layout_principal, 
            element_justification='c',
            finalize=True
        )

        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == '0':
                retorno = '0' 
                break
            
            retorno = event 
            break
        
        window.close()
        return retorno

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """
        Substitui o 'input' por um Pop-up gráfico.
        """
        titulo = "Sucesso" if sucesso else "Erro"
        sg.popup(msg, title=titulo, keep_on_top=True)