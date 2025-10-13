import os
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def obter_caminho_persistente():
    config_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'AgendaAvaliacoesAcademicas')
    if not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir)

        except Exception as e:
            logger.error(f"Erro ao criar diretório de configuração: {e}")

    return config_dir
