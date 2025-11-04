from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_ultima_entrada(self):
    try:
        cursor = self.conexao.cursor()
        cursor.execute('SELECT id FROM atividades ORDER BY id DESC LIMIT 1')
        resultado = cursor.fetchone()

        if resultado:
            ultima_id = resultado[0]
            cursor.execute('DELETE FROM atividades WHERE id = ?', (ultima_id,))
            self.conexao.commit()
            self.listar_atividades()
            self.update_textbox()
            QMessageBox.information(None, "Sucesso", "Última atividade removida com sucesso!")

        else:
            QMessageBox.warning(None, "Erro", "Nenhuma atividade para remover.")

    except Exception as e:
        logger.critical(f"Erro fatal ao limpar última entrada: {e}", exc_info=True)
