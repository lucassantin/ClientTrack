import FreeSimpleGUI as sg
from models.appointment import Appointment
from models.client import Client
from models.employee import Employee
from models.service import Service
from models.payment_type import PaymentType

class AppointmentView:
    def __init__(self):
        sg.theme('DarkBlue')

    def exibir_menu_agendamentos(self) -> str:
        """Exibe o menu principal de gerenciamento de agendamentos."""
        layout = [
            [sg.Text("GERENCIAR AGENDAMENTOS", font=("Helvetica", 16), justification='center', expand_x=True)],
            [sg.Button("Listar todos os agendamentos", key='1', size=(30, 2))],
            [sg.Button("Adicionar novo agendamento", key='2', size=(30, 2))],
            [sg.Button("Remarcar um agendamento", key='3', size=(30, 2))],
            [sg.Button("Cancelar um agendamento", key='4', size=(30, 2))],
            [sg.Button("Voltar", key='0', size=(15, 1), button_color=('white', 'firebrick'), pad=(0, 20))]
        ]
        
        window = sg.Window("Gerenciar Agendamentos", layout, element_justification='c')
        
        event, values = window.read()
        window.close()
        
        if event == sg.WIN_CLOSED:
            return '0'
        return event

    def _selecionar_objeto_popup(self, titulo: str, texto: str, lista_objetos: list) -> object | None:
        """Função auxiliar genérica para criar um popup de seleção."""
        # Cria uma lista de strings para exibir, usando o atributo .name
        nomes = [obj.name for obj in lista_objetos]
        
        layout = [
            [sg.Text(texto)],
            [sg.Listbox(values=nomes, size=(40, 10), key='-LIST-', enable_events=True)],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window(titulo, layout, keep_on_top=True)
        
        escolha = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Selecionar":
                if values['-LIST-']:
                    indice = window['-LIST-'].get_indexes()[0]
                    escolha = lista_objetos[indice]
                    break
                else:
                    sg.popup_error("Por favor, selecione um item.")
        
        window.close()
        return escolha

    def obter_dados_agendamento(self, clientes: list[Client], funcionarios: list[Employee], 
                                servicos: list[Service], tipos_pagamento: list[PaymentType]) -> dict | None:
        
        # --- Passo 1: Selecionar Cliente ---
        cliente_selecionado = self._selecionar_objeto_popup(
            "Selecionar Cliente", "Passo 1: Selecione o Cliente", clientes
        )
        if not cliente_selecionado: return None

        # --- Passo 2: Selecionar Serviço ---
        servico_selecionado = self._selecionar_objeto_popup(
            "Selecionar Serviço", f"Passo 2: Selecione o Serviço para {cliente_selecionado.name}", servicos
        )
        if not servico_selecionado: return None

        # --- Passo 3: Selecionar Funcionário ---
        funcionario_selecionado = self._selecionar_objeto_popup(
            "Selecionar Funcionário", f"Passo 3: Selecione o Funcionário", funcionarios
        )
        if not funcionario_selecionado: return None

        # --- Passo 4: Selecionar Tipo de Pagamento ---
        tipo_pagamento_selecionado = self._selecionar_objeto_popup(
            "Selecionar Pagamento", f"Passo 4: Selecione o Tipo de Pagamento", tipos_pagamento
        )
        if not tipo_pagamento_selecionado: return None

        # --- PASSO 5: CORREÇÃO APLICADA AQUI ---
        # O argumento 'tooltip' foi removido e a dica de formato foi movida para a mensagem principal.
        data_hora = sg.popup_get_text(
            "Digite a data e hora do agendamento (AAAA-MM-DD HH:MM):", 
            title="Passo 5: Data e Hora"
        )
        if not data_hora: return None

        return {
            "client": cliente_selecionado,
            "service": servico_selecionado,
            "employee": funcionario_selecionado,
            "appointment_date": data_hora,
            "payment_type": tipo_pagamento_selecionado
        }

    def exibir_lista_agendamentos(self, appointments: list[Appointment]):
        if not appointments:
            sg.popup("Nenhum agendamento encontrado.")
            return

        dados_tabela = []
        for apt in appointments:
            pagamento_str = "N/A"
            if apt.payment:
                pagamento_str = f"R$ {apt.payment.value:.2f} ({apt.payment.payment_type.name})"
                
            dados_tabela.append([
                apt.appointment_date,
                apt.client.name,
                apt.service.name,
                apt.employee.name,
                pagamento_str
            ])

        cabecalho = ["Data/Hora", "Cliente", "Serviço", "Funcionário", "Pagamento"]
        
        layout = [
            [sg.Text("LISTA DE AGENDAMENTOS", font=("Helvetica", 14))],
            [sg.Table(values=dados_tabela, headings=cabecalho, 
                      auto_size_columns=False, col_widths=[16, 20, 20, 20, 20],
                      justification='left', num_rows=20, key='-TABLE-')],
            [sg.Button("Fechar")]
        ]
        
        window = sg.Window("Lista de Agendamentos", layout)
        window.read()
        window.close()

    def obter_escolha_agendamento(self, appointments: list[Appointment], acao: str) -> Appointment | None:
        if not appointments:
            sg.popup_error(f"Nenhum agendamento para {acao}.")
            return None
            
        nomes_agendamentos = [
            f"{apt.appointment_date} | {apt.client.name} | {apt.service.name}" 
            for apt in appointments
        ]
        
        layout = [
            [sg.Text(f"Selecione um agendamento para {acao}:")],
            [sg.Listbox(values=nomes_agendamentos, size=(50, 10), key='-LIST-', enable_events=True)],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Selecionar Agendamento", layout)
        
        escolha = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Selecionar":
                if values['-LIST-']:
                    indice = window['-LIST-'].get_indexes()[0]
                    escolha = appointments[indice]
                    break
                else:
                    sg.popup_error("Por favor, selecione um agendamento na lista.")
        
        window.close()
        return escolha

    def obter_nova_data_remarcacao(self, appointment: Appointment) -> str | None:
        layout = [
            [sg.Text(f"Remarcando agendamento de: {appointment.client.name}")],
            [sg.Text(f"Data Atual: {appointment.appointment_date}")],
            [sg.Text("Nova Data (AAAA-MM-DD HH:MM):", size=(25,1)), sg.InputText(key='-DATA-')],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]
        
        window = sg.Window("Remarcar Agendamento", layout)
        nova_data = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            if event == "Salvar":
                nova_data = values['-DATA-']
                if not nova_data.strip():
                    sg.popup_error("A data não pode estar vazia.")
                else:
                    break
        
        window.close()
        return nova_data

    def confirmar_cancelamento(self, appointment: Appointment) -> bool:
        msg = (
            f"Tem certeza que deseja CANCELAR este agendamento?\n"
            f"Esta ação também excluirá o pagamento associado.\n\n"
            f"Data: {appointment.appointment_date}\n"
            f"Cliente: {appointment.client.name}\n"
            f"Serviço: {appointment.service.name}"
        )
        resposta = sg.popup_yes_no(msg, title="Confirmar Cancelamento")
        return resposta == "Yes"

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        titulo = "Sucesso" if sucesso else "Erro"
        if not sucesso:
            sg.popup_error(msg, title=titulo, keep_on_top=True)
        else:
            sg.popup(msg, title=titulo, keep_on_top=True)