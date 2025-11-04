import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QCalendarWidget, QDialogButtonBox, QMessageBox
from PySide6.QtCore import QDate, QLocale, QCoreApplication
from PySide6.QtGui import QIcon
from utils.IconUtils import get_icon_path
from source.BancoDeDados.Banco_Dados import obter_avaliacoes, lista_avaliacoes, obter_turmas, lista_turmas, obter_estrutura_cursos, traduzir_curso, traduzir_ementa, traduzir_semestre, obter_disciplinas
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def editar_detalhes_atividade(self, atividade):
    try:
        _translate = QCoreApplication.translate
        dialog = QDialog()

        try:
            icon_path = get_icon_path("ReviewsManager.ico")
            if icon_path and os.path.exists(icon_path):
                dialog.setWindowIcon(QIcon(icon_path))

        except Exception:
            pass

        dialog.setWindowTitle(_translate("InterfaceGerenciadorAtividades", "Editar Detalhes da Atividade"))
        layout = QVBoxLayout()

        label_data = QLabel(_translate("InterfaceGerenciadorAtividades", "Data:"))
        entry_data = QCalendarWidget()

        try:
            if hasattr(self, "calendar") and self.calendar is not None:
                entry_data.setLocale(self.calendar.locale())

            else:
                entry_data.setLocale(QLocale(QLocale.Portuguese))

        except Exception:
            pass

        entry_data.setSelectedDate(QDate.fromString(atividade.get('data', ''), 'dd/MM/yyyy'))
        layout.addWidget(label_data)
        layout.addWidget(entry_data)

        label_tipo = QLabel(_translate("InterfaceGerenciadorAtividades", "Tipo:"))
        entry_tipo = QComboBox()

        try:
            entry_tipo.addItems(obter_avaliacoes())

        except Exception:
            entry_tipo.addItems(lista_avaliacoes)

        entry_tipo.setCurrentText(atividade.get('tipo', ''))
        layout.addWidget(label_tipo)
        layout.addWidget(entry_tipo)

        label_sequencia = QLabel(_translate("InterfaceGerenciadorAtividades", "Sequência:"))
        entry_sequencia = QComboBox()
        entry_sequencia.addItems([""] + [str(i) for i in range(1, 11)])
        entry_sequencia.setCurrentText(atividade.get('sequencia', ''))
        layout.addWidget(label_sequencia)
        layout.addWidget(entry_sequencia)

        label_nome = QLabel(_translate("InterfaceGerenciadorAtividades", "Nome:"))
        entry_nome = QComboBox()

        try:
            from source.BancoDeDados.Banco_Dados import CURSOS_PT, CURSOS_EN

            def buscar_e_retornar_disciplinas_no_idioma_atual(nome_procurado):
                if not nome_procurado:
                    return []

                alvo = nome_procurado.strip().lower()
                import re

                grupos_encontrados = []
                for estrutura in (CURSOS_PT, CURSOS_EN):
                    for curso_key, ementas in estrutura.items():
                        for ementa_key, semestres in ementas.items():
                            if not isinstance(semestres, dict):
                                continue

                            for semestre_key, disciplinas in semestres.items():
                                for d in disciplinas:
                                    if not d:
                                        continue

                                    if d.strip().lower() == alvo:
                                        grupos_encontrados.append((curso_key, ementa_key, semestre_key))
                                        continue

                                    mm = re.search(r"([A-Z]{1,3}\d{3,4})$", d.strip(), flags=re.IGNORECASE)
                                    if mm:
                                        m2 = re.search(r"([A-Z]{1,3}\d{3,4})$", nome_procurado.strip(), flags=re.IGNORECASE)
                                        if m2 and mm.group(1).lower() == m2.group(1).lower():
                                            grupos_encontrados.append((curso_key, ementa_key, semestre_key))

                for curso_key, ementa_key, semestre_key in grupos_encontrados:
                    try:
                        curso_trad = traduzir_curso(curso_key)
                        ementa_trad = traduzir_ementa(ementa_key)
                        semestre_trad = traduzir_semestre(semestre_key)
                        disciplinas_atual = obter_disciplinas(curso_trad, ementa_trad, semestre_trad) or []
                        if disciplinas_atual:
                            return list(disciplinas_atual)

                    except Exception:
                        pass

                    try:
                        disciplinas_orig = obter_disciplinas(curso_key, ementa_key, semestre_key) or []
                        if disciplinas_orig:
                            return list(disciplinas_orig)

                    except Exception:
                        pass

                    try:
                        estrut = obter_estrutura_cursos()
                        for c_key, ements in estrut.items():
                            for e_key, sems in ements.items():
                                if not isinstance(sems, dict):
                                    continue

                                for s_key, discs in sems.items():
                                    for disc in discs:
                                        if not disc:
                                            continue

                                        if disc.strip().lower() == alvo:
                                            return list(discs)

                                        mm = re.search(r"([A-Z]{1,3}\d{3,4})$", disc.strip(), flags=re.IGNORECASE)
                                        if mm:
                                            m2 = re.search(r"([A-Z]{1,3}\d{3,4})$", nome_procurado.strip(), flags=re.IGNORECASE)
                                            if m2 and mm.group(1).lower() == m2.group(1).lower():
                                                return list(discs)

                    except Exception:
                        pass

                try:
                    estrut_atual = obter_estrutura_cursos()
                    for curso_key, ementas in estrut_atual.items():
                        for ementa_key, semestres in ementas.items():
                            if not isinstance(semestres, dict):
                                continue

                            for semestre_key, disciplinas in semestres.items():
                                for d in disciplinas:
                                    if not d:
                                        continue

                                    if d.strip().lower() == alvo:
                                        return list(disciplinas)

                                    mm = re.search(r"([A-Z]{1,3}\d{3,4})$", d.strip(), flags=re.IGNORECASE)
                                    if mm:
                                        m2 = re.search(r"([A-Z]{1,3}\d{3,4})$", nome_procurado.strip(), flags=re.IGNORECASE)
                                        if m2 and mm.group(1).lower() == m2.group(1).lower():
                                            return list(disciplinas)

                except Exception:
                    pass

                return []

            lista_encontrada = buscar_e_retornar_disciplinas_no_idioma_atual(atividade.get('nome', '')) or [atividade.get('nome', '')]

        except Exception:
            lista_encontrada = [atividade.get('nome', '')]

        entry_nome.addItems([""] + list(lista_encontrada))
        entry_nome.setCurrentText(atividade.get('nome', ''))
        layout.addWidget(label_nome)
        layout.addWidget(entry_nome)

        label_turma = QLabel(_translate("InterfaceGerenciadorAtividades", "Turma:"))
        entry_turma = QComboBox()

        try:
            entry_turma.addItems(obter_turmas())

        except Exception:
            entry_turma.addItems(lista_turmas)

        entry_turma.setCurrentText(atividade.get('turma', ''))
        layout.addWidget(label_turma)
        layout.addWidget(entry_turma)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        if dialog.exec():
            novos_dados = {
                "data": entry_data.selectedDate().toString("dd/MM/yyyy"),
                "tipo": entry_tipo.currentText(),
                "sequencia": entry_sequencia.currentText(),
                "nome": entry_nome.currentText(),
                "turma": entry_turma.currentText(),
            }

            if self.atualizar_atividade(atividade, novos_dados):
                self.update_textbox()

            else:
                QMessageBox.warning(
                    None,
                    _translate("InterfaceGerenciadorAtividades", "Erro"),
                    _translate("InterfaceGerenciadorAtividades", "Erro ao atualizar a atividade."),
                )

    except Exception as e:
        logger.critical(f"Erro fatal ao editar detalhes da atividade: {e}", exc_info=True)
