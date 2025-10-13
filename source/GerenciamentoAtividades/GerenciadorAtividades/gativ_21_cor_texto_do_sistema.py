from utils.LogManager import LogManager
logger = LogManager.get_logger()

def _cor_texto_do_sistema(self):
    try:
        if hasattr(self, "textbox") and self.textbox is not None:
            color = self.textbox.palette().color(self.textbox.palette().TextRole)

        else:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtGui import QPalette
            color = QApplication.palette().color(QPalette.Text)

        return color.name()

    except Exception:
        return "#000000"
