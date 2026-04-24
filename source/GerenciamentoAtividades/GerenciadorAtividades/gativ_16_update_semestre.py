from source.utils.LogManager import LogManager
from source.utils.ComboBoxUtils import substituir_itens_combo
logger = LogManager.get_logger()

def update_semestre(self):
    try:
        from source.BancoDeDados.Banco_Dados import obter_semestres

        selected_curso = self.combo_curso.currentText()
        selected_ementa = self.entry_ementa.currentText()
        semestres = obter_semestres(selected_curso, selected_ementa) or []
        substituir_itens_combo(self.entry_semestre, [""] + list(semestres))
        self.update_disciplinas()

    except Exception as e:
        logger.critical(f"Erro fatal ao atualizar semestre: {e}", exc_info=True)
