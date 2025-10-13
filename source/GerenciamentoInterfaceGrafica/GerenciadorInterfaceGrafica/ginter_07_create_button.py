from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_button(self):
    try:
        button = QPushButton()
        button.setMinimumWidth(12.5 * button.fontMetrics().horizontalAdvance('m'))
        button.setMaximumWidth(12.5 * button.fontMetrics().horizontalAdvance('m'))
        button.setFont(QFont('Arial', 9))
        return button

    except Exception as e:
        logger.critical(f"Erro fatal ao criar botão: {e}", exc_info=True)
