from datetime import datetime
from source.BancoDeDados.Banco_Dados import obter_cor_por_nome
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def update_textbox(self):
    try:
        atividades = self.listar_atividades()
        atividades.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

        linhas_formatadas = []

        for atividade in atividades:
            if not (atividade['tipo'] and atividade['sequencia'] and atividade['nome'] and atividade['turma']):
                continue

            nome_disciplina = atividade['nome']

            if getattr(self, "modo_cores", "preto") == "preto":
                nome_disciplina_formatado = nome_disciplina
                underline_style = ""

            else:
                cor = obter_cor_por_nome(nome_disciplina)
                if cor:
                    nome_disciplina_formatado = f"<span style='color: {cor};'>{nome_disciplina}</span>"
                    underline_style = f"style='text-decoration-color: {cor};'"

                else:
                    nome_disciplina_formatado = nome_disciplina
                    underline_style = ""

            data_formatada = f"<b>{atividade['data']}</b>" if atividade['data'] else ""
            linha = f"<u {underline_style}>{data_formatada}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['tipo']} – {atividade['sequencia']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{nome_disciplina_formatado}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['turma']}</u>"
            linha = linha.strip()
            linhas_formatadas.append(linha)

        texto_formatado = "<br><br>".join(linhas_formatadas)
        self.textbox.setHtml(texto_formatado)

    except Exception as e:
        logger.error(f"Erro ao atualizar textbox: {e}", exc_info=True)
