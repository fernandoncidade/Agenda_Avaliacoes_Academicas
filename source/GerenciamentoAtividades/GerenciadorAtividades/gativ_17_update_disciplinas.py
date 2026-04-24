from source.utils.LogManager import LogManager
from source.utils.ComboBoxUtils import substituir_itens_combo
logger = LogManager.get_logger()

def update_disciplinas(self):
    try:
        from source.BancoDeDados.Banco_Dados import obter_disciplinas

        selected_curso = self.combo_curso.currentText()
        selected_ementa = self.entry_ementa.currentText()
        selected_semestre = self.entry_semestre.currentText()
        disciplinas = obter_disciplinas(selected_curso, selected_ementa, selected_semestre) or []
        substituir_itens_combo(self.entry_disciplina, [""] + list(disciplinas))

    except Exception as e:
        logger.critical(f"Erro fatal ao atualizar disciplinas: {e}", exc_info=True)
