from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox
from datetime import datetime
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def excluir_item(self):
    try:
        dialog = QDialog()
        dialog.setWindowTitle("Excluir Item(ns)")
        layout = QVBoxLayout()

        checkboxes = []
        atividades = self.listar_atividades()
        atividades.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

        for atividade in atividades:
            if not (atividade['tipo'] and atividade['sequencia'] and atividade['nome'] and atividade['turma']):
                continue

            linha = f"{atividade['data']} {atividade['tipo']} – {atividade['sequencia']} {atividade['nome']} {atividade['turma']}"

            checkbox = QCheckBox(linha)
            checkboxes.append((checkbox, atividade))
            layout.addWidget(checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        if dialog.exec():
            for checkbox, atividade in checkboxes:
                if checkbox.isChecked():
                    self.remover_atividade(atividade)

            self.update_textbox()

    except Exception as e:
        logger.critical(f"Erro fatal ao excluir item: {e}", exc_info=True)
