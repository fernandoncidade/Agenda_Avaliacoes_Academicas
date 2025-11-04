from PySide6.QtCore import QDate
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_entradas(self):
    try:
        self.combo_curso.setCurrentIndex(0)
        self.entry_ementa.clear()
        self.entry_semestre.clear()
        self.entry_disciplina.clear()
        self.entry_codigo.setCurrentIndex(0)
        self.combo_tipo.setCurrentIndex(0)
        self.combo_sequencia.setCurrentIndex(0)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.textbox.clear()
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM atividades')
        self.conexao.commit()

    except Exception as e:
        logger.critical(f"Erro fatal ao limpar entradas: {e}", exc_info=True)
