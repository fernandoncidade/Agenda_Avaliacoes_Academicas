from collections.abc import Iterable
from PySide6.QtWidgets import QComboBox


def _normalizar_texto(texto: str | None) -> str:
    return str(texto or "").strip().casefold()


def configurar_combo_texto_livre(combo) -> None:
    if combo is None:
        return

    combo.setEditable(True)
    combo.setInsertPolicy(QComboBox.NoInsert)

    line_edit = combo.lineEdit()
    if line_edit is not None:
        line_edit.setClearButtonEnabled(True)


def obter_itens_combo(combo) -> list[str]:
    if combo is None:
        return []

    return [combo.itemText(i) for i in range(combo.count())]


def combo_contem_texto(combo, texto: str | None) -> bool:
    texto_normalizado = _normalizar_texto(texto)
    if not texto_normalizado:
        return True

    return any(_normalizar_texto(item) == texto_normalizado for item in obter_itens_combo(combo))


def adicionar_item_combo_se_ausente(combo, texto: str | None) -> None:
    if combo is None:
        return

    texto = str(texto or "").strip()
    if not texto:
        return

    sinais_bloqueados = combo.blockSignals(True)
    try:
        if not combo_contem_texto(combo, texto):
            combo.addItem(texto)

        combo.setCurrentText(texto)

    finally:
        combo.blockSignals(sinais_bloqueados)


def substituir_itens_combo(combo, itens: Iterable[str] | None, texto_atual: str | None = None) -> None:
    if combo is None:
        return

    sinais_bloqueados = combo.blockSignals(True)
    try:
        combo.clear()
        combo.addItems(list(itens or []))
        if texto_atual:
            adicionar_item_combo_se_ausente(combo, texto_atual)

    finally:
        combo.blockSignals(sinais_bloqueados)
