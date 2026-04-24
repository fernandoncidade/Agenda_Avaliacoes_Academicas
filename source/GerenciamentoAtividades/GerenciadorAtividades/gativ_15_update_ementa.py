from source.utils.LogManager import LogManager
from source.utils.ComboBoxUtils import substituir_itens_combo
logger = LogManager.get_logger()

def update_ementa(self):
    try:
        from source.BancoDeDados.Banco_Dados import obter_ementas

        selected_curso = self.combo_curso.currentText()
        ementas = obter_ementas(selected_curso) or []
        substituir_itens_combo(self.entry_ementa, [""] + list(ementas))
        self.update_semestre()

    except Exception as e:
        logger.critical(f"Erro fatal ao atualizar ementa: {e}", exc_info=True)
