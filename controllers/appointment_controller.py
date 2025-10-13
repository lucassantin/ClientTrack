from views.manager_mod_view.agendamento_view.appointment_view import AppointmentView
from DAO.appointment_dao import AppointmentSqliteDAO
from DAO.client_dao import ClientSqliteDAO
from DAO.employee_dao import EmployeeSqliteDAO
from DAO.service_dao import ServiceSqliteDAO
from DAO.payment_dao import PaymentSqliteDAO
from DAO.payment_type_dao import PaymentTypeSqliteDAO
from models.appointment import Appointment
from models.payment import Payment

class AppointmentController:
    def __init__(self):
        self.view = AppointmentView()
        self.appointment_dao = AppointmentSqliteDAO()
        self.client_dao = ClientSqliteDAO()
        self.employee_dao = EmployeeSqliteDAO()
        self.service_dao = ServiceSqliteDAO()
        self.payment_dao = PaymentSqliteDAO()
        self.payment_type_dao = PaymentTypeSqliteDAO()

    def iniciar(self):
        while True:
            opcao = self.view.exibir_menu_agendamentos()
            match opcao:
                case '1': self._listar()
                case '2': self._adicionar()
                case '3': self._remarcar()
                case '4': self._cancelar()
                case '0': break
                case _: self.view.exibir_mensagem("Opção inválida.", sucesso=False)

    def _listar(self):
        agendamentos = self.appointment_dao.find_all()
        self.view.exibir_lista_agendamentos(agendamentos)

    def _adicionar(self):
        try:
            clientes = self.client_dao.find_all() 
            funcionarios = self.employee_dao.find_all()
            servicos = self.service_dao.find_all()
            tipos_pagamento = self.payment_type_dao.find_all()
            
            if not all([clientes, funcionarios, servicos, tipos_pagamento]):
                self.view.exibir_mensagem("Faltam dados essenciais para criar um agendamento (clientes, funcionários, serviços ou tipos de pagamento).", sucesso=False)
                return

            dados = self.view.obter_dados_agendamento(clientes, funcionarios, servicos, tipos_pagamento)
            if not dados:
                self.view.exibir_mensagem("Criação de agendamento cancelada.", sucesso=False)
                return

            novo_pagamento = Payment(
                value=dados['service'].price,
                payment_type=dados['payment_type'] 
            )
            self.payment_dao.create(novo_pagamento)

            novo_agendamento = Appointment(
                client=dados['client'],
                service=dados['service'],
                employee=dados['employee'],
                appointment_date=dados['appointment_date'],
                payment=novo_pagamento
            )
            self.appointment_dao.create(novo_agendamento)
            
            cliente = dados['client']
            cliente.increment_indice()
            self.client_dao.update_indice(cliente.id, cliente.accumulatedIndice)

            self.view.exibir_mensagem("Agendamento criado com sucesso!")
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível criar agendamento: {e}", sucesso=False)

    def _remarcar(self):
        agendamentos = self.appointment_dao.find_all()
        apt_selecionado = self.view.obter_escolha_agendamento(agendamentos, "remarcar")
        if not apt_selecionado:
            return

        nova_data = self.view.obter_nova_data_remarcacao(apt_selecionado)
        if not nova_data:
            self.view.exibir_mensagem("Remarcação cancelada.", sucesso=False)
            return
        
        try:
            apt_selecionado.appointment_date = nova_data
            self.appointment_dao.update(apt_selecionado)
            self.view.exibir_mensagem("Agendamento remarcado com sucesso!")
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível remarcar: {e}", sucesso=False)

    def _cancelar(self):
        agendamentos = self.appointment_dao.find_all()
        apt_selecionado = self.view.obter_escolha_agendamento(agendamentos, "cancelar")
        if not apt_selecionado:
            return
            
        if self.view.confirmar_cancelamento(apt_selecionado):
            try:
                if apt_selecionado.payment:
                    self.payment_dao.delete(apt_selecionado.payment.id)
                
                self.appointment_dao.delete(apt_selecionado.id)
                self.view.exibir_mensagem("Agendamento cancelado com sucesso!")
            except Exception as e:
                self.view.exibir_mensagem(f"Não foi possível cancelar: {e}", sucesso=False)
        else:
            self.view.exibir_mensagem("Operação de cancelamento abortada.", sucesso=False)