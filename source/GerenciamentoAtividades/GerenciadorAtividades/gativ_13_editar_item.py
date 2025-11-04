import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox
from PySide6.QtCore import QCoreApplication
from datetime import datetime
from source.BancoDeDados.Banco_Dados import obter_avaliacoes, obter_turmas
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def editar_item(self):
    try:
        _translate = QCoreApplication.translate
        dialog = QDialog()

        try:
            from utils.IconUtils import get_icon_path
            from PySide6.QtGui import QIcon
            icon_path = get_icon_path("ReviewsManager.ico")
            if icon_path and os.path.exists(icon_path):
                dialog.setWindowIcon(QIcon(icon_path))

        except Exception:
            pass

        dialog.setWindowTitle(_translate("InterfaceGerenciadorAtividades", "Editar Item(ns)"))
        layout = QVBoxLayout()

        checkboxes = []
        atividades = self.listar_atividades()
        atividades.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

        for atividade in atividades:
            if not (atividade['tipo'] and atividade['sequencia'] and atividade['nome'] and atividade['turma']):
                continue

            try:
                tipos_atual = obter_avaliacoes()
                tipo_local = next((t for t in tipos_atual if t.strip().lower() == atividade['tipo'].strip().lower()), None)
                if not tipo_local:
                    tipo_local = atividade['tipo']

            except Exception:
                tipo_local = atividade['tipo']

            try:
                turmas_atual = obter_turmas()
                turma_local = next((t for t in turmas_atual if t.strip().lower() == atividade['turma'].strip().lower()), atividade['turma'])

            except Exception:
                turma_local = atividade['turma']

            linha = f"{atividade['data']} {tipo_local} – {atividade['sequencia']} {atividade['nome']} {turma_local}"

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
                    self.editar_detalhes_atividade(atividade)

            self.update_textbox()

    except Exception as e:
        logger.critical(f"Erro fatal ao editar item: {e}", exc_info=True)
