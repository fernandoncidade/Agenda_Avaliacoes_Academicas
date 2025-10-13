from utils.LogManager import LogManager
logger = LogManager.get_logger()

def update_semestre(self):
    try:
        from source.BancoDeDados.Banco_Dados import obter_semestres

        selected_curso = self.combo_curso.currentText()
        selected_ementa = self.entry_ementa.currentText()
        semestres = obter_semestres(selected_curso, selected_ementa) or []
        self.entry_semestre.clear()
        self.entry_semestre.addItems([""] + list(semestres))

    except Exception as e:
        logger.critical(f"Erro fatal ao atualizar semestre: {e}", exc_info=True)
