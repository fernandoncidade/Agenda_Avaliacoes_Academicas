from utils.LogManager import LogManager
logger = LogManager.get_logger()

def update_ementa(self):
    try:
        from source.BancoDeDados.Banco_Dados import obter_ementas

        selected_curso = self.combo_curso.currentText()
        ementas = obter_ementas(selected_curso) or []
        self.entry_ementa.clear()
        self.entry_ementa.addItems([""] + list(ementas))

    except Exception as e:
        logger.critical(f"Erro fatal ao atualizar ementa: {e}", exc_info=True)
