import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox
from source.BancoDeDados.Banco_Dados import obter_idioma_atual
from source.BancoDeDados.Listas_Personalizadas import (
    listar_itens_personalizados_para_exclusao,
    remover_item_personalizado,
)
from source.utils.IconUtils import get_icon_path
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

CATEGORIAS_EXCLUSAO_LISTAS = [
    ("curso", "Curso:"),
    ("ementa", "Ementa:"),
    ("semestre", "Semestre:"),
    ("disciplina", "Disciplina:"),
    ("turma", "Turma da Disciplina:"),
    ("tipo", "Tipo de Atividade Avaliativa:"),
    ("sequencia", "Sequência da Atividade:"),
]


def _aplicar_icone(dialog):
    try:
        icon_path = get_icon_path("ReviewsManager.ico")
        if icon_path and os.path.exists(icon_path):
            dialog.setWindowIcon(QIcon(icon_path))

    except Exception:
        pass


def _atualizar_interface(parent):
    try:
        if hasattr(parent, "retranslate_ui"):
            parent.retranslate_ui()

    except Exception as e:
        logger.error(f"Erro ao atualizar interface após excluir item personalizado: {e}", exc_info=True)


def _confirmar_exclusao(parent, texto_item):
    _translate = QCoreApplication.translate
    mensagem = QMessageBox(parent)
    _aplicar_icone(mensagem)
    mensagem.setIcon(QMessageBox.Question)
    mensagem.setWindowTitle(_translate("InterfaceGerenciadorAtividades", "Confirmar exclusão"))
    mensagem.setText(_translate("InterfaceGerenciadorAtividades", "Deseja remover o item selecionado?"))
    mensagem.setInformativeText(texto_item)
    mensagem.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    mensagem.setDefaultButton(QMessageBox.No)
    botao_sim = mensagem.button(QMessageBox.Yes)
    botao_nao = mensagem.button(QMessageBox.No)
    if botao_sim:
        botao_sim.setText(_translate("InterfaceGerenciadorAtividades", "Sim"))

    if botao_nao:
        botao_nao.setText(_translate("InterfaceGerenciadorAtividades", "Não"))

    return mensagem.exec() == QMessageBox.Yes


def _remover_item_do_menu(parent, menu, dados):
    try:
        _translate = QCoreApplication.translate
        if not _confirmar_exclusao(parent, dados["texto"]):
            return

        if remover_item_personalizado(dados["categoria"], dados["id"]):
            popular_menu_itens_personalizados(parent, menu, dados["categoria"])
            _atualizar_interface(parent)
            QMessageBox.information(
                parent,
                _translate("InterfaceGerenciadorAtividades", "Item excluído"),
                _translate("InterfaceGerenciadorAtividades", "O item foi excluído."),
            )
            return

        QMessageBox.warning(
            parent,
            _translate("InterfaceGerenciadorAtividades", "Erro"),
            _translate("InterfaceGerenciadorAtividades", "Não foi possível excluir o item."),
        )

    except Exception as e:
        logger.error(f"Erro ao remover item personalizado pelo menu: {e}", exc_info=True)
        QMessageBox.critical(parent, QCoreApplication.translate("InterfaceGerenciadorAtividades", "Erro"), str(e))


def popular_menu_itens_personalizados(parent, menu, categoria):
    try:
        _translate = QCoreApplication.translate
        menu.clear()

        itens = listar_itens_personalizados_para_exclusao(categoria, obter_idioma_atual())
        if not itens:
            action = menu.addAction(_translate("InterfaceGerenciadorAtividades", "Nenhum item personalizado encontrado."))
            action.setEnabled(False)
            return

        for item in itens:
            action = menu.addAction(item["texto"])
            action.triggered.connect(lambda checked=False, dados=item, m=menu: _remover_item_do_menu(parent, m, dados))

    except Exception as e:
        logger.error(f"Erro ao popular menu de itens personalizados: {e}", exc_info=True)
        menu.clear()
        action = menu.addAction(QCoreApplication.translate("InterfaceGerenciadorAtividades", "Erro"))
        action.setEnabled(False)
