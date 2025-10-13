from utils.LogManager import LogManager

logger = LogManager.get_logger()

def change_language(self, codigo_idioma):
    try:
        success = self.gerenciador_traducao.definir_idioma(codigo_idioma)
        if success:
            self.retranslate_ui()
            for c, a in self.lang_actions.items():
                a.setChecked(c == codigo_idioma)

        else:
            atual = self.gerenciador_traducao.obter_idioma_atual()
            if atual in self.lang_actions:
                self.lang_actions[atual].setChecked(True)

    except Exception as e:
        logger.critical(f"Erro fatal ao mudar idioma: {e}", exc_info=True)
