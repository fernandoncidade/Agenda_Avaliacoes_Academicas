from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager

logger = LogManager.get_logger()

try:
    from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_03_exibir_sobre import exibir_sobre

except Exception:
    exibir_sobre = None

def create_menu(self):
    try:
        menubar = self.menuBar()
        _translate = QCoreApplication.translate
        self.menu_arquivo = menubar.addMenu(_translate("InterfaceGerenciadorAtividades", "Arquivo"))

        self.action_excluir_item = QAction(_translate("InterfaceGerenciadorAtividades", "Excluir Item(ns)"), self)
        self.action_excluir_item.triggered.connect(self.excluir_item)
        self.menu_arquivo.addAction(self.action_excluir_item)

        self.action_limpar_ultima = QAction(_translate("InterfaceGerenciadorAtividades", "Limpar Última Entrada"), self)
        self.action_limpar_ultima.triggered.connect(self.limpar_ultima_entrada)
        self.menu_arquivo.addAction(self.action_limpar_ultima)

        self.action_limpar_tudo = QAction(_translate("InterfaceGerenciadorAtividades", "Limpar Tudo"), self)
        self.action_limpar_tudo.triggered.connect(self.limpar_entradas)
        self.menu_arquivo.addAction(self.action_limpar_tudo)

        self.action_editar_item = QAction(_translate("InterfaceGerenciadorAtividades", "Editar Item(ns)"), self)
        self.action_editar_item.triggered.connect(self.editar_item)
        self.menu_arquivo.addAction(self.action_editar_item)

        self.action_registrar = QAction(_translate("InterfaceGerenciadorAtividades", "Registrar Definições"), self)
        self.action_registrar.triggered.connect(self.submiter)
        self.menu_arquivo.addAction(self.action_registrar)

        self.action_export_pdf = QAction(_translate("InterfaceGerenciadorAtividades", "Exportar para PDF"), self)
        self.action_export_pdf.triggered.connect(self.exportar_para_pdf)
        self.menu_arquivo.addAction(self.action_export_pdf)

        self.menu_arquivo.addSeparator()

        self.action_sair = QAction(_translate("InterfaceGerenciadorAtividades", "Sair"), self)
        self.action_sair.triggered.connect(lambda: QCoreApplication.instance().quit())
        self.menu_arquivo.addAction(self.action_sair)

        self.menu_config = menubar.addMenu(_translate("InterfaceGerenciadorAtividades", "Configurações"))
        self.menu_idiomas = self.menu_config.addMenu(_translate("InterfaceGerenciadorAtividades", "Idiomas"))

        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.setExclusive(True)
        self.lang_actions = {}

        try:
            for codigo, nome in self.gerenciador_traducao.idiomas_disponiveis.items():
                action = QAction(_translate("InterfaceGerenciadorAtividades", nome), self)
                action.setCheckable(True)
                action.setData(codigo)
                action.triggered.connect(lambda checked, c=codigo: self.change_language(c))
                self.menu_idiomas.addAction(action)
                self.lang_action_group.addAction(action)
                self.lang_actions[codigo] = action

            atual = self.gerenciador_traducao.obter_idioma_atual()
            if atual in self.lang_actions:
                self.lang_actions[atual].setChecked(True)

        except Exception as e:
            logger.critical(f"Erro fatal ao criar ações de idioma: {e}", exc_info=True)

        try:
            self.menu_cores = self.menu_config.addMenu(_translate("InterfaceGerenciadorAtividades", "Cores"))
            self.color_action_group = QActionGroup(self)
            self.color_action_group.setExclusive(True)
            self.color_actions = {}

            for codigo, nome_label in [("preto", _translate("InterfaceGerenciadorAtividades", "Preto")),
                                       ("coloridas", _translate("InterfaceGerenciadorAtividades", "Coloridas"))]:
                action = QAction(nome_label, self)
                action.setCheckable(True)
                action.setData(codigo)
                action.triggered.connect(lambda checked, c=codigo: self.change_color_mode(c))
                self.menu_cores.addAction(action)
                self.color_action_group.addAction(action)
                self.color_actions[codigo] = action

            modo_atual = None
            if hasattr(self, 'gerenciamento_atividades'):
                try:
                    modo_atual = self.gerenciamento_atividades.obter_modo_cores()

                except Exception:
                    modo_atual = None

            if modo_atual in self.color_actions:
                self.color_actions[modo_atual].setChecked(True)

        except Exception as e:
            logger.critical(f"Erro fatal ao criar ações de cores: {e}", exc_info=True)

        self.menu_sobre = menubar.addMenu(_translate("InterfaceGerenciadorAtividades", "Sobre"))
        self.action_sobre = QAction(_translate("InterfaceGerenciadorAtividades", "Sobre"), self)

        def _on_sobre():
            try:
                if exibir_sobre:
                    exibir_sobre(self)

                else:
                    QMessageBox.information(self, _translate("InterfaceGerenciadorAtividades", "Sobre"),
                                            _translate("InterfaceGerenciadorAtividades", "Informação não disponível"))

            except Exception as e:
                logger.error(f"Erro ao abrir diálogo Sobre: {e}", exc_info=True)
                QMessageBox.critical(self, _translate("InterfaceGerenciadorAtividades", "Erro"), str(e))

        self.action_sobre.triggered.connect(_on_sobre)
        self.menu_sobre.addAction(self.action_sobre)

    except Exception as e:
        logger.critical(f"Erro fatal ao criar menu: {e}", exc_info=True)
