from views.manager_mod_view.serviços_view.especiality_view import EspecialityView
from DAO.specialty_dao import SpecialtySqliteDAO
from models.specialty import Specialty

class EspecialityController:
    def __init__(self):
        self.view = EspecialityView()
        self.dao = SpecialtySqliteDAO()

    def iniciar(self):
        """Inicia o loop do menu de gerenciamento de especialidades."""
        while True:
            opcao = self.view.exibir_menu_especialidades()

            match opcao:
                case '1': self._listar()
                case '2': self._adicionar()
                case '3': self._atualizar()
                case '4': self._deletar()
                case '0': break
                case _: self.view.exibir_mensagem("Opção inválida.", sucesso=False)

    def _listar(self):
        especialidades = self.dao.find_all()
        self.view.exibir_lista_especialidades(especialidades)

    def _adicionar(self):
        dados = self.view.obter_dados_especialidade()
        if not dados:
            return

        try:
            nova_especialidade = Specialty(
                name=dados.get("nome"),
                description=dados.get("descricao")
            )
            self.dao.create(nova_especialidade)
            self.view.exibir_mensagem("Especialidade adicionada com sucesso!")
        except (TypeError, ValueError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível adicionar: {e}", sucesso=False)

    def _atualizar(self):
        especialidades = self.dao.find_all()
        if not especialidades:
            self.view.exibir_mensagem("Nenhuma especialidade para atualizar.", sucesso=False)
            return

        esp_selecionada = self.view.obter_escolha_especialidade(especialidades, "atualizar")
        if not esp_selecionada:
            return

        novos_dados = self.view.obter_novos_dados_para_atualizar(esp_selecionada)
        
        try:
            esp_selecionada.name = novos_dados.get("nome")
            esp_selecionada.description = novos_dados.get("descricao")

            self.dao.update(esp_selecionada)
            self.view.exibir_mensagem("Especialidade atualizada com sucesso!")
        except (TypeError, ValueError) as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível atualizar: {e}", sucesso=False)

    def _deletar(self):
        especialidades = self.dao.find_all()
        if not especialidades:
            self.view.exibir_mensagem("Nenhuma especialidade para deletar.", sucesso=False)
            return

        esp_selecionada = self.view.obter_escolha_especialidade(especialidades, "deletar")
        if not esp_selecionada:
            return

        if self.view.confirmar_exclusao(esp_selecionada.name):
            try:
                self.dao.delete(esp_selecionada.id)
                self.view.exibir_mensagem("Especialidade deletada com sucesso!")
            except Exception as e:
                self.view.exibir_mensagem(f"Não foi possível deletar: {e}", sucesso=False)