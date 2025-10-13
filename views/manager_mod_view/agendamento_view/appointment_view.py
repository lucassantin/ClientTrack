import os
from models.appointment import Appointment
from models.client import Client
from models.employee import Employee
from models.service import Service
from models.payment_type import PaymentType

class AppointmentView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_agendamentos(self) -> str:
        self.limpar_tela()
        print("====== GERENCIAR AGENDAMENTOS ======\n")
        print("  1. Listar todos os agendamentos")
        print("  2. Adicionar novo agendamento")
        print("  3. Remarcar um agendamento")
        print("  4. Cancelar um agendamento")
        print("\n  0. Voltar")
        print("\n==================================")
        return input("Escolha uma opção: ")

    def obter_dados_agendamento(self, clientes: list[Client], funcionarios: list[Employee], servicos: list[Service], tipos_pagamento: list[PaymentType]) -> dict | None:
        self.limpar_tela()
        print("====== NOVO AGENDAMENTO ======\n")
        
        try:
            print("--- 1. Selecione o Cliente ---")
            for i, c in enumerate(clientes): print(f"  {i+1}. {c.name}")
            print("  0. Cancelar")
            cliente_idx = int(input("\nEscolha o cliente: "))
            if cliente_idx == 0: return None
            cliente_selecionado = clientes[cliente_idx - 1]
            
            print("\n--- 2. Selecione o Serviço ---")
            for i, s in enumerate(servicos): print(f"  {i+1}. {s.name} (R$ {s.price:.2f})")
            print("  0. Cancelar")
            servico_idx = int(input("\nEscolha o serviço: "))
            if servico_idx == 0: return None
            servico_selecionado = servicos[servico_idx - 1]

            print("\n--- 3. Selecione o Funcionário ---")
            for i, f in enumerate(funcionarios): print(f"  {i+1}. {f.name}")
            print("  0. Cancelar")
            funcionario_idx = int(input("\nEscolha o funcionário: "))
            if funcionario_idx == 0: return None
            funcionario_selecionado = funcionarios[funcionario_idx - 1]

            data_hora = input("\n--- 4. Digite a data e hora (AAAA-MM-DD HH:MM): ")
            if not data_hora: return None
            
            print("\n--- 5. Selecione o Tipo de Pagamento ---")
            for i, pt in enumerate(tipos_pagamento): print(f"  {i+1}. {pt.name}")
            print("  0. Cancelar")
            tipo_pagamento_idx = int(input("\nEscolha o tipo de pagamento: "))
            if tipo_pagamento_idx == 0: return None
            tipo_pagamento_selecionado = tipos_pagamento[tipo_pagamento_idx - 1]

            return {
                "client": cliente_selecionado,
                "service": servico_selecionado,
                "employee": funcionario_selecionado,
                "appointment_date": data_hora,
                "payment_type": tipo_pagamento_selecionado
            }
        except (ValueError, IndexError):
            self.exibir_mensagem("Seleção inválida. Operação cancelada.", sucesso=False)
            return None

    def exibir_lista_agendamentos(self, appointments: list[Appointment]):
        self.limpar_tela()
        print("======================== LISTA DE AGENDAMENTOS ========================\n")
        if not appointments:
            print("Nenhum agendamento encontrado.")
        else:
            for apt in appointments:
                print(f"Data: {apt.appointment_date} | Cliente: {apt.client.name}")
                print(f"  Serviço: {apt.service.name} com {apt.employee.name}")
                if apt.payment:
                    print(f"  Pagamento: R$ {apt.payment.value:.2f} via {apt.payment.payment_type.name}")
                else:
                    print("  Pagamento: (Não encontrado)")
                print("-" * 60)
        input("\nPressione Enter para continuar...")

    def obter_escolha_agendamento(self, appointments: list[Appointment], acao: str) -> Appointment | None:
        self.limpar_tela()
        print(f"====== SELECIONE UM AGENDAMENTO PARA {acao.upper()} ======\n")
        if not appointments:
            self.exibir_mensagem("Nenhum agendamento para selecionar.", sucesso=False)
            return None
            
        for i, apt in enumerate(appointments):
            print(f"  {i + 1}. {apt.appointment_date} - {apt.client.name} - {apt.service.name}")
        print("\n  0. Cancelar")
        
        while True:
            try:
                escolha = int(input("\nDigite o número do agendamento: "))
                if 0 <= escolha <= len(appointments):
                    return None if escolha == 0 else appointments[escolha - 1]
                print("Número inválido.")
            except ValueError:
                print("Entrada inválida.")

    def obter_nova_data_remarcacao(self, appointment: Appointment) -> str | None:
        self.limpar_tela()
        print("====== REMARCAR AGENDAMENTO ======")
        print(f"Data atual: {appointment.appointment_date}")
        nova_data = input("Digite a nova data e hora (AAAA-MM-DD HH:MM) ou [Enter] para cancelar: ")
        return nova_data if nova_data.strip() else None

    def confirmar_cancelamento(self, appointment: Appointment) -> bool:
        self.limpar_tela()
        print("====== CANCELAR AGENDAMENTO ======")
        print("Atenção: Esta ação é irreversível e também excluirá o pagamento associado.\n")
        print(f"  Data: {appointment.appointment_date}")
        print(f"  Cliente: {appointment.client.name}")
        print(f"  Serviço: {appointment.service.name}\n")
        confirmacao = input("Tem certeza que deseja cancelar este agendamento? (s/n): ").lower()
        return confirmacao == 's'

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")