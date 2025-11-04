from utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_atividade(self, atividade, novos_dados):
    try:
        chave_unica_antiga = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        chave_unica_nova = (novos_dados['data'], novos_dados['tipo'], novos_dados['sequencia'], novos_dados['nome'], novos_dados['turma'])

        if chave_unica_antiga in self.atividades:
            del self.atividades[chave_unica_antiga]

            self.atividades[chave_unica_nova] = novos_dados

            cursor = self.conexao.cursor()
            cursor.execute('''
                UPDATE atividades
                SET data = ?, tipo = ?, sequencia = ?, nome = ?, turma = ?
                WHERE data = ? AND tipo = ? AND sequencia = ? AND nome = ? AND turma = ?
            ''', (novos_dados['data'], novos_dados['tipo'], novos_dados['sequencia'], novos_dados['nome'], novos_dados['turma'],
                atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma']))
            self.conexao.commit()

            self.update_textbox()
            return True

        return False

    except Exception as e:
        logger.error(f"Erro ao atualizar atividade: {e}", exc_info=True)
