from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QDate
from source.BancoDeDados.Banco_Dados import registrar_valores_personalizados
from source.utils.ComboBoxUtils import adicionar_item_combo_se_ausente, combo_contem_texto
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _texto_combo(combo):
    if combo is None:
        return ""

    return combo.currentText().strip()

def submiter(self):
    try:
        data = self.calendar.selectedDate().toString('dd/MM/yyyy')
        curso = _texto_combo(self.combo_curso)
        ementa = _texto_combo(self.entry_ementa)
        semestre = _texto_combo(self.entry_semestre)
        tipo = _texto_combo(self.combo_tipo)
        sequencia = _texto_combo(self.combo_sequencia)
        nome = _texto_combo(self.entry_disciplina)
        turma = _texto_combo(self.entry_codigo)

        if tipo and sequencia and nome and turma:
            registrar_curso = bool(curso) and not combo_contem_texto(self.combo_curso, curso)
            registrar_ementa = bool(curso and ementa) and not combo_contem_texto(self.entry_ementa, ementa)
            registrar_semestre = bool(curso and ementa and semestre) and not combo_contem_texto(self.entry_semestre, semestre)
            registrar_disciplina = bool(curso and ementa and semestre and nome) and not combo_contem_texto(self.entry_disciplina, nome)
            registrar_turma = bool(turma) and not combo_contem_texto(self.entry_codigo, turma)
            registrar_tipo = bool(tipo) and not combo_contem_texto(self.combo_tipo, tipo)
            registrar_sequencia = bool(sequencia) and not combo_contem_texto(self.combo_sequencia, sequencia)

            registrar_valores_personalizados(
                curso=curso,
                ementa=ementa,
                semestre=semestre,
                disciplina=nome,
                turma=turma,
                tipo=tipo,
                sequencia=sequencia,
                registrar_curso=registrar_curso,
                registrar_ementa=registrar_ementa,
                registrar_semestre=registrar_semestre,
                registrar_disciplina=registrar_disciplina,
                registrar_turma=registrar_turma,
                registrar_tipo=registrar_tipo,
                registrar_sequencia=registrar_sequencia,
            )

            adicionar_item_combo_se_ausente(self.combo_curso, curso)
            adicionar_item_combo_se_ausente(self.entry_ementa, ementa)
            adicionar_item_combo_se_ausente(self.entry_semestre, semestre)
            adicionar_item_combo_se_ausente(self.entry_disciplina, nome)
            adicionar_item_combo_se_ausente(self.entry_codigo, turma)
            adicionar_item_combo_se_ausente(self.combo_tipo, tipo)
            adicionar_item_combo_se_ausente(self.combo_sequencia, sequencia)

            atividade = {
                'data': data,
                'tipo': tipo,
                'sequencia': sequencia,
                'nome': nome,
                'turma': turma
            }
            self.adicionar_atividade(atividade)
            self.update_textbox()

        else:
            QMessageBox.warning(None, "Erro", "Por favor, preencha todas as informações antes de adicionar a atividade.")

    except Exception as e:
        logger.error(f"Erro ao submeter atividade: {e}", exc_info=True)
