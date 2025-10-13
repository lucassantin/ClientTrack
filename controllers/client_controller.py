from views.authentication_mod_view.client_view import ClientView
from DAO.client_dao import ClientSqliteDAO
from models.client import Client

class ClientController:
    """Controller para o CRUD de Clientes."""
    def __init__(self):
        self.view = ClientView()
        self.dao = ClientSqliteDAO()

    def iniciar(self):
        while True:
            opcao = self.view.exibir_menu_clientes()
            match opcao:
                case '1': self._listar()
                case '2': self._adicionar()
                case '3': self._atualizar()
                case '4': self._deletar()
                case '5': self._verificar_status()
                case '6': self._resgatar_insight()
                case '0': break
                case _: self.view.exibir_mensagem("Opção inválida.", sucesso=False)

    def _listar(self):
        clientes = self.dao.find_all()
        self.view.exibir_lista_clientes(clientes)

    def _adicionar(self):
        dados = self.view.obter_dados_cliente()
        if not dados:
            return

        try:
            indice_int = int(dados['indice'])
            novo_cliente = Client(
                name=dados['name'],
                contact=dados['contact'],
                birthDay=dados['birthDay'] or None,
                indice=indice_int,
                recommendation=dados['recommendation']
            )
            self.dao.create(novo_cliente)
            self.view.exibir_mensagem("Cliente adicionado com sucesso!")
        except (ValueError, TypeError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível adicionar cliente: {e}", sucesso=False)
            
    def _atualizar(self):
        clientes = self.dao.find_all()
        if not clientes:
            self.view.exibir_mensagem("Nenhum cliente para atualizar.", sucesso=False)
            return

        cliente_selecionado = self.view.obter_escolha_cliente(clientes, "atualizar")
        if not cliente_selecionado:
            return

        novos_dados = self.view.obter_novos_dados_para_atualizar(cliente_selecionado)
        
        try:
            cliente_selecionado.name = novos_dados['name']
            cliente_selecionado.contact = novos_dados['contact']
            cliente_selecionado.birthDay = novos_dados['birthDay'] or None
            
            cliente_selecionado.insight.indice = int(novos_dados['indice'])
            cliente_selecionado.insight.recommendation = novos_dados['recommendation']
            
            self.dao.update(cliente_selecionado)
            self.view.exibir_mensagem("Cliente atualizado com sucesso!")
        except (ValueError, TypeError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível atualizar: {e}", sucesso=False)

    def _deletar(self):
        clientes = self.dao.find_all()
        if not clientes:
            self.view.exibir_mensagem("Nenhum cliente para deletar.", sucesso=False)
            return

        cliente_selecionado = self.view.obter_escolha_cliente(clientes, "deletar")
        if not cliente_selecionado:
            return

        if self.view.confirmar_exclusao(cliente_selecionado.name):
            try:
                if self.dao.delete(cliente_selecionado.id):
                    self.view.exibir_mensagem("Cliente deletado com sucesso!")
                else:
                    self.view.exibir_mensagem("Erro: Cliente não encontrado para deletar.", sucesso=False)
            except Exception as e:
                self.view.exibir_mensagem(f"Não foi possível deletar: {e}", sucesso=False)

    def _verificar_status(self):
        clientes = self.dao.find_all()
        cliente_selecionado = self.view.obter_escolha_cliente(clientes, "verificar o status")
        if not cliente_selecionado:
            return
        
        self.view.exibir_status_insight(cliente_selecionado)

    def _resgatar_insight(self):
        clientes = self.dao.find_all()
        cliente_selecionado = self.view.obter_escolha_cliente(clientes, "resgatar um insight")
        if not cliente_selecionado:
            return

        if not cliente_selecionado.insight:
            self.view.exibir_mensagem("Este cliente não possui um insight configurado.", sucesso=False)
            return
            
        if not cliente_selecionado.can_redeem():
            pontos_faltantes = cliente_selecionado.insight.indice - cliente_selecionado.accumulatedIndice
            msg = f"Pontos insuficientes. Faltam {pontos_faltantes} ponto(s)."
            self.view.exibir_mensagem(msg, sucesso=False)
            return

        if self.view.confirmar_resgate(cliente_selecionado):
            try:
                recomendacao = cliente_selecionado.redeem_insight()
                self.dao.update_indice(cliente_selecionado.id, cliente_selecionado.accumulatedIndice)
                
                msg = (f"Insight resgatado com sucesso!\n\n"
                       f"Recomendação: '{recomendacao}'\n"
                       f"Novo saldo de pontos: {cliente_selecionado.accumulatedIndice}")
                self.view.exibir_mensagem(msg)
            except (ValueError, Exception) as e:
                self.view.exibir_mensagem(f"Não foi possível resgatar: {e}", sucesso=False)
        else:
            self.view.exibir_mensagem("Resgate cancelado.", sucesso=False)