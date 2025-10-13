from views.reports.report_view import ReportView
from DAO.appointment_dao import AppointmentSqliteDAO

class ReportController:
    def __init__(self):
        self.view = ReportView()
        self.appointment_dao = AppointmentSqliteDAO()

    def iniciar(self):
        """Inicia o loop do menu de relatórios."""
        while True:
            opcao = self.view.exibir_menu_relatorios()
            match opcao:
                case '1': self._relatorio_servicos()
                case '2': self._relatorio_clientes()
                case '3': self._relatorio_funcionarios()
                case '4': self._relatorio_clientes_inativos()
                case '0': break
                case _: self.view.exibir_mensagem("Opção inválida.", sucesso=False)
    
    def _relatorio_servicos(self):
        dados = self.appointment_dao.get_most_used_services()
        self.view.exibir_relatorio_simples(
            "Serviços Mais Consumidos", dados, "name", "total"
        )

    def _relatorio_clientes(self):
        dados = self.appointment_dao.get_most_frequent_clients()
        self.view.exibir_relatorio_simples(
            "Clientes Mais Frequentes", dados, "name", "total"
        )

    def _relatorio_funcionarios(self):
        dados = self.appointment_dao.get_busiest_employees()
        self.view.exibir_relatorio_simples(
            "Funcionários com Mais Atendimentos", dados, "name", "total"
        )

    def _relatorio_clientes_inativos(self):
        dados = self.appointment_dao.get_inactive_clients()
        self.view.exibir_relatorio_clientes_inativos(dados)