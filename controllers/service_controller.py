from views.manager_mod_view.serviços_view.service_view import ServiceView
from DAO.service_dao import ServiceSqliteDAO
from DAO.specialty_dao import SpecialtySqliteDAO
from models.service import Service

class ServiceController:
    def __init__(self):
        self.view = ServiceView()
        self.dao = ServiceSqliteDAO()
        self.specialty_dao = SpecialtySqliteDAO()

    def iniciar(self):
        """Inicia o loop do menu de gerenciamento de serviços."""
        while True:
            opcao = self.view.exibir_menu_servicos()

            if opcao == '1':
                self._listar()
            elif opcao == '2':
                self._adicionar()
            elif opcao == '3':
                self._atualizar()
            elif opcao == '4':
                self._deletar()
            elif opcao == '0':
                break
            else:
                self.view.exibir_mensagem("Opção inválida.", sucesso=False)

    def _listar(self):
        servicos = self.dao.find_all()
        self.view.exibir_lista_servicos(servicos)

    def _adicionar(self):
        dados = self.view.obter_dados_servico()
        if not dados: 
            return

        try:
            preco = float(dados.get("preco").replace(',', '.'))
            
            novo_servico = Service(
                name=dados.get("nome"),
                description=dados.get("descricao"),
                price=preco
            )
            self.dao.create(novo_servico)
            self.view.exibir_mensagem("Serviço adicionado com sucesso!")

        except (TypeError, ValueError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível adicionar o serviço: {e}", sucesso=False)

    def _atualizar(self):
        servicos = self.dao.find_all()
        if not servicos:
            self.view.exibir_mensagem("Nenhum serviço para atualizar.", sucesso=False)
            return

        servico_selecionado = self.view.obter_escolha_servico(servicos, "atualizar")
        if not servico_selecionado:
            return

        especialidades_disponiveis = self.specialty_dao.find_all()
        novos_dados = self.view.obter_novos_dados_para_atualizar(servico_selecionado, especialidades_disponiveis)
        
        try:
            servico_selecionado.name = novos_dados.get("nome")
            servico_selecionado.description = novos_dados.get("descricao")
            servico_selecionado.price = float(str(novos_dados.get("preco")).replace(',', '.'))
            servico_selecionado.specialty = novos_dados.get("especialidade") 
            
            self.dao.update(servico_selecionado)
            self.view.exibir_mensagem("Serviço atualizado com sucesso!")
        except (TypeError, ValueError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível atualizar: {e}", sucesso=False)


    def _deletar(self):
        """Orquestra a exclusão de um serviço."""
        servicos = self.dao.find_all()
        if not servicos:
            self.view.exibir_mensagem("Nenhum serviço para deletar.", sucesso=False)
            return

        servico_selecionado = self.view.obter_escolha_servico(servicos, "deletar")
        if not servico_selecionado:
            return 

        if self.view.confirmar_exclusao(servico_selecionado.name):
            try:
                if self.dao.delete(servico_selecionado.id):
                    self.view.exibir_mensagem("Serviço deletado com sucesso!")
                else:
                    self.view.exibir_mensagem("Serviço não encontrado no banco de dados.", sucesso=False)
            except Exception as e:
                self.view.exibir_mensagem(f"Não foi possível deletar o serviço: {e}", sucesso=False)