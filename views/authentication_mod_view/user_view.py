import FreeSimpleGUI as sg

class UserView:
    """View gráfica para o menu principal do módulo de usuários."""
    
    def __init__(self):
        sg.theme('DarkBlue') 

    def exibir_menu_usuarios(self) -> str:
        """
        Exibe o menu de gerenciamento de usuários.
        Retorna a chave ('key') do botão clicado.
        """
        layout = [
            [sg.Text("GERENCIAR USUÁRIOS", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Gerenciar Clientes", key='1', size=(30, 2))],
            [sg.Button("Gerenciar Funcionários", key='2', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]

        window = sg.Window("Gerenciar Usuários", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
            
        return event

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe um popup de mensagem."""
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo, keep_on_top=True)
        else:
            sg.popup(msg, title=titulo, keep_on_top=True)