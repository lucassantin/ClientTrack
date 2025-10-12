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
        cliente_selecionado = self.view.obter_escolha_cliente(clientes, "atualizar")
        if not cliente_selecionado:
            return

        novos_dados = self.view.obter_novos_dados_para_atualizar(cliente_selecionado)
        if not novos_dados:
            return
            
        try:
            cliente_selecionado.name = novos_dados['name']
            cliente_selecionado.contact = novos_dados['contact']
            cliente_selecionado.birthDay = novos_dados['birthDay'] or None
            
            self.dao.update(cliente_selecionado)
            self.view.exibir_mensagem("Cliente atualizado com sucesso!")
        except (ValueError, TypeError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível atualizar: {e}", sucesso=False)

    def _deletar(self):
        clientes = self.dao.find_all()
        cliente_selecionado = self.view.obter_escolha_cliente(clientes, "deletar")
        if not cliente_selecionado:
            return

        if self.view.confirmar_exclusao(cliente_selecionado.name):
            if self.dao.delete(cliente_selecionado.id):
                self.view.exibir_mensagem("Cliente deletado com sucesso!")
            else:
                self.view.exibir_mensagem("Erro ao deletar cliente.", sucesso=False)