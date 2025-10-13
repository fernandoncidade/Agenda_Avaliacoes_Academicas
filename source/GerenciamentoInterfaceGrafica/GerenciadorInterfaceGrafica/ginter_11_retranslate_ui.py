from PySide6.QtCore import QCoreApplication, QLocale
from source.BancoDeDados.Banco_Dados import obter_cursos, obter_turmas, obter_avaliacoes
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def retranslate_ui(self):
    try:
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("InterfaceGerenciadorAtividades", "Cadastro de Atividades Avaliativas"))

        self.label_curso.setText(_translate("InterfaceGerenciadorAtividades", "Curso:"))
        self.label_ementa.setText(_translate("InterfaceGerenciadorAtividades", "Ementa:"))
        self.label_semestre.setText(_translate("InterfaceGerenciadorAtividades", "Semestre:"))
        self.label_disciplina.setText(_translate("InterfaceGerenciadorAtividades", "Disciplina:"))
        self.label_codigo.setText(_translate("InterfaceGerenciadorAtividades", "Turma da Disciplina:"))
        self.label_tipo.setText(_translate("InterfaceGerenciadorAtividades", "Tipo de Atividade Avaliativa:"))
        self.label_sequencia.setText(_translate("InterfaceGerenciadorAtividades", "Sequência da Atividade:"))
        self.label_data.setText(_translate("InterfaceGerenciadorAtividades", "Defina a Data da Atividade:"))
        self.label_banco_dados.setText(_translate("InterfaceGerenciadorAtividades", "Caixa de Dados:"))

        self.button_clear_item.setText(_translate("InterfaceGerenciadorAtividades", "Excluir Item(ns)"))
        self.button_clear_ultima.setText(_translate("InterfaceGerenciadorAtividades", "Limpar Última Entrada"))
        self.button_clear.setText(_translate("InterfaceGerenciadorAtividades", "Limpar Tudo"))
        self.button_editar_item.setText(_translate("InterfaceGerenciadorAtividades", "Editar Item(ns)"))
        self.button_submiter.setText(_translate("InterfaceGerenciadorAtividades", "Registrar Definições"))
        self.button_export.setText(_translate("InterfaceGerenciadorAtividades", "Exportar para PDF"))

        try:
            if hasattr(self, 'menu_config'):
                self.menu_config.setTitle(_translate("InterfaceGerenciadorAtividades", "Configurações"))

            if hasattr(self, 'menu_idiomas'):
                self.menu_idiomas.setTitle(_translate("InterfaceGerenciadorAtividades", "Idiomas"))

            if hasattr(self, 'menu_arquivo'):
                self.menu_arquivo.setTitle(_translate("InterfaceGerenciadorAtividades", "Arquivo"))

            if hasattr(self, 'action_export_pdf'):
                self.action_export_pdf.setText(_translate("InterfaceGerenciadorAtividades", "Exportar para PDF"))

            if hasattr(self, 'action_excluir_item'):
                self.action_excluir_item.setText(_translate("InterfaceGerenciadorAtividades", "Excluir Item(ns)"))

            if hasattr(self, 'action_limpar_ultima'):
                self.action_limpar_ultima.setText(_translate("InterfaceGerenciadorAtividades", "Limpar Última Entrada"))

            if hasattr(self, 'action_limpar_tudo'):
                self.action_limpar_tudo.setText(_translate("InterfaceGerenciadorAtividades", "Limpar Tudo"))

            if hasattr(self, 'action_editar_item'):
                self.action_editar_item.setText(_translate("InterfaceGerenciadorAtividades", "Editar Item(ns)"))

            if hasattr(self, 'action_registrar'):
                self.action_registrar.setText(_translate("InterfaceGerenciadorAtividades", "Registrar Definições"))

            if hasattr(self, 'action_sair'):
                self.action_sair.setText(_translate("InterfaceGerenciadorAtividades", "Sair"))

            if hasattr(self, 'menu_sobre'):
                self.menu_sobre.setTitle(_translate("InterfaceGerenciadorAtividades", "Sobre"))

            if hasattr(self, 'action_sobre'):
                self.action_sobre.setText(_translate("InterfaceGerenciadorAtividades", "Sobre"))

            if hasattr(self, 'menu_cores'):
                self.menu_cores.setTitle(_translate("InterfaceGerenciadorAtividades", "Cores"))

            if hasattr(self, 'color_actions'):
                if 'preto' in self.color_actions:
                    self.color_actions['preto'].setText(_translate("InterfaceGerenciadorAtividades", "Preto"))

                if 'coloridas' in self.color_actions:
                    self.color_actions['coloridas'].setText(_translate("InterfaceGerenciadorAtividades", "Coloridas"))

        except Exception as e:
            logger.error(f"Erro ao configurar menus: {e}", exc_info=True)

        try:
            idioma_atual = None
            if hasattr(self, 'gerenciador_traducao'):
                idioma_atual = self.gerenciador_traducao.obter_idioma_atual()

            if idioma_atual and idioma_atual.lower().startswith('pt'):
                self.calendar.setLocale(QLocale(QLocale.Portuguese))

            else:
                self.calendar.setLocale(QLocale(QLocale.English))

            self.calendar.update()

        except Exception as e:
            logger.error(f"Erro ao atualizar calendário: {e}", exc_info=True)

        self.combo_curso.clear()
        self.combo_curso.addItems(obter_cursos())

        self.entry_codigo.clear()
        self.entry_codigo.addItems(obter_turmas())

        self.combo_tipo.clear()
        self.combo_tipo.addItems(obter_avaliacoes())

        try:
            if hasattr(self, 'lang_actions') and hasattr(self, 'gerenciador_traducao'):
                for codigo, nome in self.gerenciador_traducao.idiomas_disponiveis.items():
                    if codigo in self.lang_actions:
                        self.lang_actions[codigo].setText(_translate("InterfaceGerenciadorAtividades", nome))

        except Exception as e:
            logger.error(f"Erro ao atualizar rótulos de idiomas: {e}", exc_info=True)

    except Exception as e:
        logger.critical(f"Erro fatal ao retraduzir UI: {e}", exc_info=True)
