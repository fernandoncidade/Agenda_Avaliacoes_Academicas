from utils.LogManager import LogManager
logger = LogManager.get_logger()

def buscar_atividade(self, atividade):
    try:
        chave_unica = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        return self.atividades.get(chave_unica, None)

    except Exception as e:
        logger.error(f"Erro ao buscar atividade: {e}", exc_info=True)
