import os
from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from source.GerenciamentoAtividades.Gerenciador_Atividades import GerenciamentoAtividades
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_04_center_on_screen import center_on_screen
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_05_showEvent import showEvent
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_06_create_widgets import create_widgets
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_07_create_button import create_button
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_08_create_menu import create_menu
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_09_change_language import change_language
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_10_change_color_mode import change_color_mode
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_11_retranslate_ui import retranslate_ui
from language.tr_01_gerenciadorTraducao import GerenciadorTraducao
from utils.IconUtils import get_icon_path
from utils.LogManager import LogManager

logger = LogManager.get_logger()

try:
    from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_03_exibir_sobre import exibir_sobre

except Exception:
    exibir_sobre = None


class InterfaceGerenciadorAtividades(QMainWindow):
    def __init__(self, gerenciador_traducao: GerenciadorTraducao | None = None):
        super().__init__()
        try:
            self.gerenciamento_atividades = GerenciamentoAtividades()
            self.gerenciador_traducao = gerenciador_traducao or GerenciadorTraducao()

            try:
                self.gerenciador_traducao.aplicar_traducao()

            except Exception:
                pass

            self.gerenciador_traducao.idioma_alterado.connect(self.retranslate_ui)

            icon_title_path = get_icon_path("ReviewsManager.ico") or get_icon_path("Reviews-Manager_PySide6-pyppeteer.1.0.ico")
            if icon_title_path and os.path.exists(icon_title_path):
                self.setWindowIcon(QtGui.QIcon(icon_title_path))

            self.setWindowTitle("")

            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.layout = QVBoxLayout(self.central_widget)

            self.create_widgets()
            self.create_menu()
            self.retranslate_ui()
            self.update_textbox()
        
        except Exception as e:
            logger.critical(f"Erro fatal ao inicializar InterfaceGerenciadorAtividades: {e}", exc_info=True)

    center_on_screen = center_on_screen
    showEvent = showEvent
    create_widgets = create_widgets
    create_button = create_button
    create_menu = create_menu
    change_language = change_language
    change_color_mode = change_color_mode
    retranslate_ui = retranslate_ui

    def submiter(self):
        try:
            self.gerenciamento_atividades.submiter()

        except Exception as e:
            logger.critical(f"Erro fatal ao submeter: {e}", exc_info=True)

    def limpar_entradas(self):
        try:
            self.gerenciamento_atividades.limpar_entradas()

        except Exception as e:
            logger.critical(f"Erro fatal ao limpar entradas: {e}", exc_info=True)

    def limpar_ultima_entrada(self):
        try:
            self.gerenciamento_atividades.limpar_ultima_entrada()

        except Exception as e:
            logger.critical(f"Erro fatal ao limpar última entrada: {e}", exc_info=True)

    def excluir_item(self):
        try:
            self.gerenciamento_atividades.excluir_item()

        except Exception as e:
            logger.critical(f"Erro fatal ao excluir item: {e}", exc_info=True)

    def editar_item(self):
        try:
            self.gerenciamento_atividades.editar_item()

        except Exception as e:
            logger.critical(f"Erro fatal ao editar item: {e}", exc_info=True)

    def exportar_para_pdf(self):
        try:
            self.gerenciamento_atividades.exportar_para_pdf()

        except Exception as e:
            logger.critical(f"Erro fatal ao exportar para PDF: {e}", exc_info=True)

    def update_textbox(self):
        try:
            self.gerenciamento_atividades.update_textbox()

        except Exception as e:
            logger.critical(f"Erro fatal ao atualizar textbox: {e}", exc_info=True)

    def update_ementa(self):
        try:
            self.gerenciamento_atividades.update_ementa()

        except Exception as e:
            logger.critical(f"Erro fatal ao atualizar ementa: {e}", exc_info=True)

    def update_semestre(self):
        try:
            self.gerenciamento_atividades.update_semestre()

        except Exception as e:
            logger.critical(f"Erro fatal ao atualizar semestre: {e}", exc_info=True)

    def update_disciplinas(self):
        try:
            self.gerenciamento_atividades.update_disciplinas()

        except Exception as e:
            logger.critical(f"Erro fatal ao atualizar disciplinas: {e}", exc_info=True)
