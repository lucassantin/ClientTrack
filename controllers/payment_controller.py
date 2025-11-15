
from views.manager_mod_view.pagamentos_view.payment_view import PaymentView
from DAO.payment_type_dao import PaymentTypeSqliteDAO
from models.payment_type import PaymentType

class PaymentController:
    def __init__(self):
        self.view = PaymentView()
        self.dao = PaymentTypeSqliteDAO()

    def gerenciar(self):
        while True:
            opcao = self.view.exibir_menu_gerenciamento()

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
        tipos_pagamento = self.dao.find_all()
        self.view.exibir_lista_tipos_pagamento(tipos_pagamento)

    def _adicionar(self):
        dados = self.view.obter_dados_tipo_pagamento()

        if dados is None:
            self.view.exibir_mensagem("Criação cancelada.", sucesso=False)
            return

        nome = dados.get("nome")

        if not nome or not nome.strip(): 
            self.view.exibir_mensagem("O nome não pode estar vazio.", sucesso=False)
            return

        try:
            novo_tipo = PaymentType(name=nome)
            self.dao.create(novo_tipo)
            self.view.exibir_mensagem("Tipo de pagamento adicionado com sucesso!")
        except TypeError as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível adicionar: {e}", sucesso=False)
            
    def _atualizar(self):
        tipos = self.dao.find_all()
        tipo_selecionado = self.view.obter_escolha_tipo(tipos, "atualizar")

        if not tipo_selecionado:
            return 

        novos_dados = self.view.obter_novos_dados_para_atualizar(tipo_selecionado)
        novo_nome = novos_dados.get("nome")

        if not novo_nome:
            return 
        
        try:
            tipo_selecionado.name = novo_nome
            self.dao.update(tipo_selecionado)
            self.view.exibir_mensagem("Tipo de pagamento atualizado com sucesso!")
        except TypeError as e:
            self.view.exibir_mensagem(f"Erro de validação: {e}", sucesso=False)
        except Exception as e:
            self.view.exibir_mensagem(f"Não foi possível atualizar: {e}", sucesso=False)

    def _deletar(self):
        """Orquestra a exclusão de um tipo de pagamento."""
        tipos = self.dao.find_all()
        tipo_selecionado = self.view.obter_escolha_tipo(tipos, "deletar")

        if not tipo_selecionado:
            return 

        if self.view.confirmar_exclusao(tipo_selecionado.name):
            try:
                if self.dao.delete(tipo_selecionado.id):
                    self.view.exibir_mensagem("Tipo de pagamento deletado com sucesso!")
                else:
                    self.view.exibir_mensagem("Tipo de pagamento não encontrado.", sucesso=False)
            except Exception as e:
                self.view.exibir_mensagem(f"Não foi possível deletar: {e}", sucesso=False)