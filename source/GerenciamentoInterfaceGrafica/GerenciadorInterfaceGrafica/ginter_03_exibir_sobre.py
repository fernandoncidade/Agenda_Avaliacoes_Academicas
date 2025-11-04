from PySide6.QtCore import QCoreApplication
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_01_SobreDialog import SobreDialog
from source.GerenciamentoInterfaceGrafica.GerenciadorInterfaceGrafica.ginter_02_OpcoesSobre import (
    SITE_LICENSES,
    LICENSE_TEXT_PT_BR, LICENSE_TEXT_EN_US,
    NOTICE_TEXT_PT_BR, NOTICE_TEXT_EN_US,
    ABOUT_TEXT_PT_BR, ABOUT_TEXT_EN_US,
    Privacy_Policy_pt_BR, Privacy_Policy_en_US,
    History_APP_pt_BR, History_APP_en_US,
    RELEASE_NOTES_pt_BR, RELEASE_NOTES_en_US
)
from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def exibir_sobre(app):
    try:
        def get_texts():
            idioma = app.gerenciador_traducao.obter_idioma_atual()
            textos_sobre = { "pt_BR": ABOUT_TEXT_PT_BR, "en_US": ABOUT_TEXT_EN_US }
            textos_licenca = { "pt_BR": LICENSE_TEXT_PT_BR, "en_US": LICENSE_TEXT_EN_US }
            textos_aviso = { "pt_BR": NOTICE_TEXT_PT_BR, "en_US": NOTICE_TEXT_EN_US }
            textos_privacidade = { "pt_BR": Privacy_Policy_pt_BR, "en_US": Privacy_Policy_en_US }
            history_texts = { "pt_BR": History_APP_pt_BR, "en_US": History_APP_en_US }
            release_notes_texts = { "pt_BR": RELEASE_NOTES_pt_BR, "en_US": RELEASE_NOTES_en_US }
            descricao_texts = {
                "pt_BR": (
                    "A Agenda de Avaliações Acadêmicas é um aplicativo leve para Windows que ajuda "
                    "estudantes e professores a organizar e visualizar todas as avaliações do semestre "
                    "(provas, testes, trabalhos, apresentações etc.) em um único lugar. "
                    "Permite cadastrar datas e detalhes das atividades, ver as tarefas em ordem "
                    "cronológica, destacar itens por cor para identificação rápida, filtrar e editar "
                    "entradas, e exportar listas em PDF para impressão ou compartilhamento. "
                    "A interface é simples, rápida de consultar e pode ser usada em Português e Inglês."
                    f"<br><br><b>{get_text('Adquira também os meus seguintes aplicativos:')}</b>"
                    "<ul>"
                    "<li><a href='https://apps.microsoft.com/detail/9NN8Z5Z700TM'>Linceu Lighthouse</a></li>"
                    "<li><a href='https://apps.microsoft.com/detail/9PJMT90R953K'>Compression Manager</a></li>"
                    "<li><a href='https://apps.microsoft.com/detail/9P289X0185C3'>Eisenhower Organizer</a></li>"
                    "</ul>"
                    "<p><i>Versão Gratuíta, permitida compartilhação!</i></p>"
                ),
                "en_US": (
                    "The Academic Evaluation Schedule is a lightweight Windows application that helps "
                    "students and teachers organize and view all semester assessments (exams, quizzes, "
                    "assignments, presentations, etc.) in one place. You can register dates and details "
                    "for activities, see them in chronological order, highlight items with colors for "
                    "quick recognition, filter and edit entries, and export lists to PDF for printing "
                    "or sharing. The interface is simple, fast to consult and available in Portuguese "
                    "and English."
                    f"<br><br><b>{get_text('Adquira também os meus seguintes aplicativos:')}</b>"
                    "<ul>"
                    "<li><a href='https://apps.microsoft.com/detail/9NN8Z5Z700TM'>Linceu Lighthouse</a></li>"
                    "<li><a href='https://apps.microsoft.com/detail/9PJMT90R953K'>Compression Manager</a></li>"
                    "<li><a href='https://apps.microsoft.com/detail/9P289X0185C3'>Eisenhower Organizer</a></li>"
                    "</ul>"
                    "<p><i>Free version, sharing allowed!</i></p>"
                )
            }
            texto_sobre = textos_sobre.get(idioma, textos_sobre["en_US"])
            texto_licenca = textos_licenca.get(idioma, textos_licenca["en_US"])
            texto_aviso = textos_aviso.get(idioma, textos_aviso["en_US"])
            texto_privacidade = textos_privacidade.get(idioma, textos_privacidade["en_US"])
            texto_history = history_texts.get(idioma, history_texts["en_US"])
            texto_release_notes = release_notes_texts.get(idioma, release_notes_texts["en_US"])
            texto_descricao = descricao_texts.get(idioma, descricao_texts["en_US"])
            cabecalho_fixo = (
                f"<h3>{QCoreApplication.translate('InterfaceGerenciadorAtividades', 'AGENDA DE AVALIAÇÕES ACADÊMICAS')}</h3>"
                f"<p><b>{get_text('Versão')}:</b> 0.0.1.0</p>"
                f"<p><b>{get_text('Autores')}:</b> Fernando Nillsson Cidade</p>"
                f"<p><b>{get_text('Descrição')}:</b> {texto_descricao}</p>"
            )

            return {
                "titulo": f"{get_text('Sobre')} - {QCoreApplication.translate('InterfaceGerenciadorAtividades', 'AGENDA DE AVALIAÇÕES ACADÊMICAS')}",
                "cabecalho_fixo": cabecalho_fixo,
                "texto_history": texto_history,
                "detalhes": texto_sobre,
                "licencas": texto_licenca,
                "sites_licencas": SITE_LICENSES,
                "show_history_text": get_text("Histórico"),
                "hide_history_text": get_text("Ocultar histórico"),
                "show_details_text": get_text("Detalhes"),
                "hide_details_text": get_text("Ocultar detalhes"),
                "show_licenses_text": get_text("Licenças"),
                "hide_licenses_text": get_text("Ocultar licenças"),
                "ok_text": QCoreApplication.translate("Dialog", "OK"),
                "site_oficial_text": get_text("Site oficial"),
                "avisos": texto_aviso,
                "show_notices_text": get_text("Avisos"),
                "hide_notices_text": get_text("Ocultar avisos"),
                "Privacy_Policy": texto_privacidade,
                "show_privacy_policy_text": get_text("Política de Privacidade"),
                "hide_privacy_policy_text": get_text("Ocultar política de privacidade"),
                "info_not_available_text": get_text("Informação não disponível"),
                "release_notes": texto_release_notes,
                "show_release_notes_text": get_text("Notas de Versão"),
                "hide_release_notes_text": get_text("Ocultar notas de versão")
            }

        if hasattr(app, "_sobre_dialog_cm") and getattr(app, "_sobre_dialog_cm") is not None:
            dlg = getattr(app, "_sobre_dialog_cm")
            if dlg.isVisible():
                dlg.retranslate_ui(get_texts())
                dlg.show()
                try:
                    dlg.raise_()

                except Exception:
                    pass

                try:
                    dlg.activateWindow()

                except Exception:
                    pass

                return

            else:
                try:
                    dlg.deleteLater()

                except Exception:
                    pass

                try:
                    setattr(app, "_sobre_dialog_cm", None)

                except Exception:
                    pass

        texts = get_texts()
        dialog = SobreDialog(
            app,
            titulo=texts["titulo"],
            texto_fixo=texts["cabecalho_fixo"],
            texto_history=texts["texto_history"],
            detalhes=texts["detalhes"],
            licencas=texts["licencas"],
            sites_licencas=texts["sites_licencas"],
            show_history_text=texts["show_history_text"],
            hide_history_text=texts["hide_history_text"],
            show_details_text=texts["show_details_text"],
            hide_details_text=texts["hide_details_text"],
            show_licenses_text=texts["show_licenses_text"],
            hide_licenses_text=texts["hide_licenses_text"],
            ok_text=texts["ok_text"],
            site_oficial_text=texts["site_oficial_text"],
            avisos=texts["avisos"],
            show_notices_text=texts["show_notices_text"],
            hide_notices_text=texts["hide_notices_text"],
            Privacy_Policy=texts["Privacy_Policy"],
            show_privacy_policy_text=texts["show_privacy_policy_text"],
            hide_privacy_policy_text=texts["hide_privacy_policy_text"],
            info_not_available_text=texts["info_not_available_text"],
            release_notes=texts["release_notes"],
            show_release_notes_text=texts["show_release_notes_text"],
            hide_release_notes_text=texts["hide_release_notes_text"]
        )

        dialog.resize(800, 700)
        try:
            setattr(app, "_sobre_dialog_cm", dialog)
            dialog.destroyed.connect(lambda _: setattr(app, "_sobre_dialog_cm", None))
            try:
                if not getattr(app, "_sobre_lang_connected", False) and hasattr(app, "gerenciador_traducao"):
                    def _recreate_sobre(_new_lang):
                        try:
                            current = getattr(app, "_sobre_dialog_cm", None)
                            if current is not None and current.isVisible():
                                current.retranslate_ui(get_texts())

                            else:
                                try:
                                    if current is not None:
                                        current.deleteLater()

                                except Exception:
                                    pass

                                try:
                                    setattr(app, "_sobre_dialog_cm", None)

                                except Exception:
                                    pass

                        except Exception:
                            pass

                    app.gerenciador_traducao.idioma_alterado.connect(_recreate_sobre)
                    setattr(app, "_sobre_lang_connected", True)

            except Exception:
                pass

        except Exception:
            pass

        dialog.show()

    except Exception as e:
        logger.error(f"Erro ao exibir diálogo Sobre: {e}", exc_info=True)
        QMessageBox.critical(app, get_text("Erro"), f"{get_text('Erro')}: {e}")
