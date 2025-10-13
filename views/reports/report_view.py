import os

class ReportView:
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_menu_relatorios(self) -> str:
        self.limpar_tela()
        print("========== MÓDULO DE RELATÓRIOS ==========\n")
        print("  1. Serviços mais consumidos")
        print("  2. Clientes mais frequentes")
        print("  3. Funcionários com mais atendimentos")
        print("  4. Clientes inativos (por último agendamento)")
        print("\n  0. Voltar")
        print("\n========================================")
        return input("Escolha um relatório: ")

    def exibir_relatorio_simples(self, titulo: str, dados: list, coluna_item: str, coluna_total: str):
        self.limpar_tela()
        print(f"====== {titulo.upper()} ======\n")
        if not dados:
            print("Nenhum dado encontrado para este relatório.")
        else:
            print(f"{'#':<3} {coluna_item.upper():<30} {coluna_total.upper()}")
            print("-" * 50)
            for i, item in enumerate(dados):
                print(f"{i+1:<3} {item[coluna_item]:<30} {item[coluna_total]}")
        
        print("\n" + "=" * 50)
        input("Pressione Enter para continuar...")

    def exibir_relatorio_clientes_inativos(self, dados: list):
        self.limpar_tela()
        print("====== RELATÓRIO DE CLIENTES INATIVOS ======\n")
        if not dados:
            print("Nenhum cliente encontrado.")
        else:
            print(f"{'CLIENTE':<25} {'CONTATO':<20} {'ÚLTIMO AGENDAMENTO':<20} {'DIAS SEM AGENDAR'}")
            print("-" * 90)
            for item in dados:
                ultimo_agendamento = item['last_appointment'] or "Nenhum"
                dias = item['days_since_last'] if item['days_since_last'] is not None else "N/A"
                print(f"{item['name']:<25} {item['contact']:<20} {ultimo_agendamento:<20} {dias}")
        
        print("\n" + "=" * 90)
        input("Pressione Enter para continuar...")

    def exibir_mensagem(self, msg: str, sucesso: bool = True):
        """Exibe uma mensagem de feedback."""
        self.limpar_tela()
        print(f"--- {'SUCESSO' if sucesso else 'ERRO'} ---\n")
        print(msg)
        print("\n--------------------")
        input("Pressione Enter para continuar...")