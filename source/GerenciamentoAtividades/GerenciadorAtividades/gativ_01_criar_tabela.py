from utils.LogManager import LogManager
logger = LogManager.get_logger()

def criar_tabela(self):
    try:
        cursor = self.conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                tipo TEXT,
                sequencia TEXT,
                nome TEXT,
                turma TEXT
            )
        ''')
        self.conexao.commit()

    except Exception as e:
        logger.error(f"Erro ao criar tabela de atividades: {e}", exc_info=True)
