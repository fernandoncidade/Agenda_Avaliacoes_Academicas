from utils.LogManager import LogManager
logger = LogManager.get_logger()

def obter_modo_cores(self):
    try:
        return getattr(self, "modo_cores", "coloridas")

    except Exception:
        return "coloridas"
