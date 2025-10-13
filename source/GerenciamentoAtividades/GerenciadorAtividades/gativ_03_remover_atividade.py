from utils.LogManager import LogManager
logger = LogManager.get_logger()

def remover_atividade(self, atividade):
    try:
        chave_unica = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        if chave_unica in self.atividades:
            del self.atividades[chave_unica]
            cursor = self.conexao.cursor()
            cursor.execute('''
                DELETE FROM atividades 
                WHERE data = ? AND tipo = ? AND sequencia = ? AND nome = ? AND turma = ?
            ''', chave_unica)
            self.conexao.commit()

    except Exception as e:
        logger.error(f"Erro ao remover atividade: {e}", exc_info=True)
