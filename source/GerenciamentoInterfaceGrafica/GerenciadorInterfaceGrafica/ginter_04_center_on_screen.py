from PySide6.QtWidgets import QApplication
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def center_on_screen(self):
    try:
        screen_geometry = QApplication.primaryScreen().geometry()
        center_point = screen_geometry.center()
        self.move(center_point - self.rect().center())

    except Exception as e:
        logger.critical(f"Erro fatal ao centralizar a janela: {e}", exc_info=True)
