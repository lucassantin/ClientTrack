import FreeSimpleGUI as sg

class AppointmentMainView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu(self) -> str:
        """
        Exibe o menu de Gerenciamento.
        Retorna a 'key' (chave) do botão clicado.
        """
        layout = [
            [sg.Text("MENU DE GERENCIAMENTO", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Gerenciar Tipos de Pagamento", key='1', size=(30, 2))],
            [sg.Button("Gerenciar Serviços", key='2', size=(30, 2))],
            [sg.Button("Gerenciar Especialidades", key='3', size=(30, 2))],
            [sg.Button("Gerenciar Agendamentos", key='4', size=(30, 2))],
            [sg.Button("Voltar ao menu principal", key='0', size=(30, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]

        window = sg.Window("Módulo de Gerenciamento", layout, element_justification='c')
        
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