from utils.LogManager import LogManager
logger = LogManager.get_logger()

def adicionar_atividade(self, atividade):
    try:
        chave_unica = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        self.atividades[chave_unica] = atividade
        cursor = self.conexao.cursor()
        cursor.execute('''
            INSERT INTO atividades (data, tipo, sequencia, nome, turma)
            VALUES (?, ?, ?, ?, ?)
        ''', (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma']))
        self.conexao.commit()

    except Exception as e:
        logger.error(f"Erro ao adicionar atividade: {e}", exc_info=True)
