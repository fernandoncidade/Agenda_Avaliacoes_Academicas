from utils.LogManager import LogManager

logger = LogManager.get_logger()

def showEvent(self, event):
    try:
        self.center_on_screen()
        super(self.__class__, self).showEvent(event)

    except Exception as e:
        logger.critical(f"Erro fatal ao exibir a janela: {e}", exc_info=True)
