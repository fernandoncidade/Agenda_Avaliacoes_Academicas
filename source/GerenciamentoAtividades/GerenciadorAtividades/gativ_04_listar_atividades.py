from utils.LogManager import LogManager
logger = LogManager.get_logger()

def listar_atividades(self):
    try:
        cursor = self.conexao.cursor()
        cursor.execute('SELECT data, tipo, sequencia, nome, turma FROM atividades')
        atividades_db = cursor.fetchall()
        self.atividades = {(a[0], a[1], a[2], a[3], a[4]): {'data': a[0], 'tipo': a[1], 'sequencia': a[2], 'nome': a[3], 'turma': a[4]} for a in atividades_db}

        return list(self.atividades.values())

    except Exception as e:
        logger.error(f"Erro ao listar atividades: {e}", exc_info=True)
