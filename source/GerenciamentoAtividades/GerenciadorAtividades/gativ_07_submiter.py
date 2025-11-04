from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QDate
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def submiter(self):
    try:
        data = self.calendar.selectedDate().toString('dd/MM/yyyy')
        tipo = self.combo_tipo.currentText()
        sequencia = self.combo_sequencia.currentText()
        nome = self.entry_disciplina.currentText()
        turma = self.entry_codigo.currentText()

        if tipo and sequencia and nome and turma:
            atividade = {
                'data': data,
                'tipo': tipo,
                'sequencia': sequencia,
                'nome': nome,
                'turma': turma
            }
            self.adicionar_atividade(atividade)
            self.update_textbox()

        else:
            QMessageBox.warning(None, "Erro", "Por favor, preencha todas as informações antes de adicionar a atividade.")

    except Exception as e:
        logger.error(f"Erro ao submeter atividade: {e}", exc_info=True)
