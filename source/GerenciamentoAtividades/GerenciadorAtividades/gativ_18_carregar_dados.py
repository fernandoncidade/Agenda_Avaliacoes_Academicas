from utils.LogManager import LogManager
logger = LogManager.get_logger()

def carregar_dados(self):
    try:
        self.listar_atividades()
        self.update_textbox()

    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}", exc_info=True)
