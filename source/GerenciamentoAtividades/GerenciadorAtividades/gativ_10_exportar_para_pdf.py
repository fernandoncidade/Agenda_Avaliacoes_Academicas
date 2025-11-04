import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from datetime import datetime
from source.BancoDeDados.Banco_Dados import obter_cor_por_nome
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def exportar_para_pdf(self):
    try:
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(None, "Salvar PDF", "", "PDF Files (*.pdf)")

        if not file_path:
            return

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=0.5*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=0.5*cm
        )
        styles = getSampleStyleSheet()
        styles['Normal'].fontSize = 10
        elements = []

        atividades = self.listar_atividades()
        atividades.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

        if not atividades:
            elements.append(Paragraph("", styles['Normal']))

        else:
            for atividade in atividades:
                if not (atividade['tipo'] and atividade['sequencia'] and atividade['nome'] and atividade['turma']):
                    continue

                nome_disciplina = atividade['nome']

                if getattr(self, "modo_cores", "preto") == "preto":
                    cor = "#000000"
                    try:
                        cor = self._cor_texto_do_sistema()

                    except Exception:
                        cor = "#000000"

                else:
                    cor = obter_cor_por_nome(nome_disciplina)

                if cor:
                    nome_disciplina_formatado = f"<b><span color='{cor}'>{nome_disciplina}</span></b>"
                    underline_style = f"color='{cor}'"

                else:
                    nome_disciplina_formatado = nome_disciplina
                    underline_style = ""

                data_formatada = f"<b>{atividade['data']}</b>" if atividade['data'] else ""
                linha = f"<u {underline_style}>{data_formatada}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['tipo']} – {atividade['sequencia']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{nome_disciplina_formatado}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['turma']}</u>"

                p = Paragraph(linha, styles['Normal'])
                elements.append(p)
                elements.append(Spacer(1, 24))

        doc.build(elements)
        QMessageBox.information(None, "Sucesso", "Atividades exportadas com sucesso para PDF!")

    except Exception as e:
        logger.critical(f"Erro fatal ao exportar para PDF: {e}", exc_info=True)
        QMessageBox.critical(None, "Erro", f"Erro ao exportar para PDF: {e}")
