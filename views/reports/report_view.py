import FreeSimpleGUI as sg

class ReportView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu_relatorios(self) -> str:
        """Exibe o menu principal do módulo de relatórios."""
        layout = [
            [sg.Text("MÓDULO DE RELATÓRIOS", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Serviços mais consumidos", key='1', size=(30, 2))],
            [sg.Button("Clientes mais frequentes", key='2', size=(30, 2))],
            [sg.Button("Funcionários com mais atendimentos", key='3', size=(30, 2))],
            [sg.Button("Clientes inativos", key='4', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]
        
        window = sg.Window("Relatórios", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
        return event

    def exibir_relatorio_simples(self, titulo: str, dados: list, coluna_item: str, coluna_total: str):
        """Exibe um popup com uma tabela simples de ranking (ex: Top Serviços)."""
        if not dados:
            sg.popup("Nenhum dado encontrado para este relatório.", title=titulo)
            return

        dados_tabela = []
        for i, item in enumerate(dados):
            dados_tabela.append([i + 1, item[coluna_item], item[coluna_total]])

        cabecalho = ["#", coluna_item.upper(), coluna_total.upper()]
        
        layout = [
            [sg.Text(titulo.upper(), font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[5, 30, 10],
                      justification='left', num_rows=15, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window(titulo, layout)
        window.read()
        window.close()

    def exibir_relatorio_clientes_inativos(self, dados: list):
        """Exibe um popup com a tabela de clientes inativos."""
        if not dados:
            sg.popup("Nenhum cliente encontrado.", title="Clientes Inativos")
            return

        dados_tabela = []
        for item in dados:
            ultimo_agendamento = item['last_appointment'] or "Nenhum"
            dias = item['days_since_last'] if item['days_since_last'] is not None else "N/A"
            dados_tabela.append([item['name'], item['contact'], ultimo_agendamento, dias])

        cabecalho = ["Cliente", "Contato", "Último Agendamento", "Dias sem Agendar"]
        
        layout = [
            [sg.Text("RELATÓRIO DE CLIENTES INATIVOS", font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[25, 20, 20, 15],
                      justification='left', num_rows=20, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window("Clientes Inativos", layout)
        window.read()
        window.close()

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe um popup de mensagem simples."""
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo, keep_on_top=True)
        else:
            sg.popup(msg, title=titulo, keep_on_top=True)