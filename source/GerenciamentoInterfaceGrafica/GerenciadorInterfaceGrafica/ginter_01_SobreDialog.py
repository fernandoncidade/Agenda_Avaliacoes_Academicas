import html
import re
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QSizePolicy, QHBoxLayout, QWidget, QTabWidget
from PySide6.QtCore import Qt
from utils.LogManager import LogManager

logger = LogManager.get_logger()


class SobreDialog(QDialog):
    def __init__(self, parent, titulo, texto_fixo, texto_history, detalhes, licencas, sites_licencas, show_history_text, hide_history_text, 
                 show_details_text, hide_details_text, show_licenses_text, hide_licenses_text, ok_text, site_oficial_text, avisos=None, 
                 show_notices_text=None, hide_notices_text=None, Privacy_Policy=None, show_privacy_policy_text=None, hide_privacy_policy_text=None, 
                 info_not_available_text="Information not available", release_notes=None, show_release_notes_text=None, hide_release_notes_text=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(titulo)
            self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
            self.setModal(False)
            self.setAttribute(Qt.WA_DeleteOnClose, True)

            self.info_not_available_text = info_not_available_text

            layout = QVBoxLayout(self)

            header_widget = QWidget()
            header_layout = QVBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(5)

            self.fixed_label = QLabel(texto_fixo)
            self.fixed_label.setTextFormat(Qt.TextFormat.RichText)
            self.fixed_label.setWordWrap(True)
            self.fixed_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.fixed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

            try:
                self.fixed_label.setOpenExternalLinks(True)

            except Exception:
                pass

            header_layout.setSpacing(0)
            self.fixed_label.setContentsMargins(0, 0, 0, 0)
            self.fixed_label.setStyleSheet("QLabel { margin: 0px; padding: 0px; }")

            try:
                if self.fixed_label.textFormat() == Qt.TextFormat.RichText:
                    txt = self.fixed_label.text()
                    self.fixed_label.setText(f'<div style="margin:0;padding:0;">{txt}</div>')

            except Exception:
                pass

            header_layout.addWidget(self.fixed_label)

            header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addWidget(header_widget)

            self.tabs = QTabWidget()
            self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            history_browser = QTextBrowser()
            history_browser.setReadOnly(True)
            history_browser.setOpenExternalLinks(True)
            self._set_browser_content(history_browser, texto_history, info_not_available_text)
            self._history_browser = history_browser
            self.tabs.addTab(history_browser, show_history_text)

            detalhes_browser = QTextBrowser()
            detalhes_browser.setReadOnly(True)
            detalhes_browser.setOpenExternalLinks(True)
            self._set_browser_content(detalhes_browser, detalhes, info_not_available_text)
            self._detalhes_browser = detalhes_browser
            self.tabs.addTab(detalhes_browser, show_details_text)

            licencas_browser = QTextBrowser()
            licencas_browser.setReadOnly(True)
            licencas_browser.setOpenExternalLinks(True)
            if licencas:
                licencas_html = self._plain_to_html(licencas)
                licencas_html += f"<br><br><h3>{site_oficial_text}</h3><ul>"
                for site in sites_licencas.strip().split('\n'):
                    if site.strip():
                        s = site.strip()
                        licencas_html += f'<li><a href="{s}">{s}</a></li>'

                licencas_html += "</ul>"
                licencas_browser.setHtml(licencas_html)

            else:
                licencas_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self._licencas_browser = licencas_browser
            self.tabs.addTab(licencas_browser, show_licenses_text)

            avisos_browser = QTextBrowser()
            avisos_browser.setReadOnly(True)
            avisos_browser.setOpenExternalLinks(True)
            self._set_browser_content(avisos_browser, avisos, info_not_available_text)
            self._avisos_browser = avisos_browser
            self.tabs.addTab(avisos_browser, show_notices_text)

            privacidade_browser = QTextBrowser()
            privacidade_browser.setReadOnly(True)
            privacidade_browser.setOpenExternalLinks(True)
            self._set_browser_content(privacidade_browser, Privacy_Policy, info_not_available_text)
            self._privacidade_browser = privacidade_browser
            self.tabs.addTab(privacidade_browser, show_privacy_policy_text)

            release_notes_browser = QTextBrowser()
            release_notes_browser.setReadOnly(True)
            release_notes_browser.setOpenExternalLinks(True)
            self._set_browser_content(release_notes_browser, release_notes, info_not_available_text)
            self._release_notes_browser = release_notes_browser
            self.tabs.addTab(release_notes_browser, show_release_notes_text or "Release Notes")

            self._show_labels = [
                show_history_text,
                show_details_text,
                show_licenses_text,
                show_notices_text,
                show_privacy_policy_text,
                show_release_notes_text or "Release Notes"
            ]

            self._hide_labels = [
                hide_history_text,
                hide_details_text,
                hide_licenses_text,
                hide_notices_text,
                hide_privacy_policy_text,
                hide_release_notes_text
            ]

            self.tabs.currentChanged.connect(self._on_tab_changed)

            self._update_tab_labels(self.tabs.currentIndex())

            layout.addWidget(self.tabs)

            button_layout = QHBoxLayout()
            self.ok_button = QPushButton(ok_text)
            self.ok_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.ok_button.clicked.connect(self.accept)
            button_layout.addStretch(1)
            button_layout.addWidget(self.ok_button)
            layout.addLayout(button_layout)

            self.setMinimumSize(400, 200)

        except Exception as e:
            logger.error(f"Erro ao criar dialog sobre: {e}", exc_info=True)

    def _plain_to_html(self, text: str) -> str:
        if not text:
            return ""

        esc = html.escape(text)
        parts = []
        lines = esc.splitlines()
        in_ul = False
        paragraph_lines = []

        def flush_paragraph():
            nonlocal paragraph_lines
            if paragraph_lines:
                parts.append("<p>" + "<br>".join(paragraph_lines) + "</p>")
                paragraph_lines = []

        for ln in lines:
            if not ln.strip():
                if in_ul:
                    parts.append("</ul>")
                    in_ul = False

                flush_paragraph()
                continue

            stripped = ln.lstrip()
            if stripped.startswith(("- ", "* ")):
                flush_paragraph()
                if not in_ul:
                    in_ul = True
                    parts.append("<ul>")

                item = stripped[2:]
                item = re.sub(r'(https?://[^\s<]+)', r'<a href="\1">\1</a>', item)
                parts.append(f"<li>{item}</li>")

            else:
                if in_ul:
                    parts.append("</ul>")
                    in_ul = False
                ln2 = re.sub(r'(https?://[^\s<]+)', r'<a href="\1">\1</a>', ln)
                paragraph_lines.append(ln2)

        if in_ul:
            parts.append("</ul>")

        flush_paragraph()
        return "".join(parts) if parts else "<p></p>"

    def _set_browser_content(self, browser: QTextBrowser, content: str, info_text: str):
        if content:
            if re.search(r'<\s*(a|p|ul|ol|li|br|b|i|strong|em|div|h[1-6])\b', content or "", re.I):
                browser.setHtml(content)

            else:
                browser.setHtml(self._plain_to_html(content))

        else:
            browser.setHtml(f"<p>{info_text}.</p>")

    def _on_tab_changed(self, index: int):
        try:
            self._update_tab_labels(index)

        except Exception:
            logger.exception("Erro ao atualizar rótulos das abas")

    def _update_tab_labels(self, current_index: int):
        for i in range(self.tabs.count()):
            if i == current_index:
                hide_label = self._hide_labels[i] if i < len(self._hide_labels) else None
                label = hide_label if hide_label else (self._show_labels[i] if i < len(self._show_labels) else "")

            else:
                label = self._show_labels[i] if i < len(self._show_labels) and self._show_labels[i] else self.tabs.tabText(i)

            self.tabs.setTabText(i, label)

    def retranslate_ui(self, texts):
        try:
            self.setWindowTitle(texts['titulo'])
            self.fixed_label.setText(f'<div style="margin:0;padding:0;">{texts["cabecalho_fixo"]}</div>')

            self._set_browser_content(self._history_browser, texts.get('texto_history'), texts.get('info_not_available_text', self.info_not_available_text))
            self.tabs.setTabText(0, texts['show_history_text'])

            self._set_browser_content(self._detalhes_browser, texts.get('detalhes'), texts.get('info_not_available_text', self.info_not_available_text))
            self.tabs.setTabText(1, texts['show_details_text'])

            licencas = texts.get('licencas')
            if licencas:
                licencas_html = self._plain_to_html(licencas)
                licencas_html += f"<br><br><h3>{texts['site_oficial_text']}</h3><ul>"
                for site in texts['sites_licencas'].strip().split('\n'):
                    if site.strip():
                        s = site.strip()
                        licencas_html += f'<li><a href="{s}">{s}</a></li>'

                licencas_html += "</ul>"
                self._licencas_browser.setHtml(licencas_html)

            else:
                self._licencas_browser.setHtml(f"<p>{texts.get('info_not_available_text', self.info_not_available_text)}.</p>")

            self.tabs.setTabText(2, texts['show_licenses_text'])

            self._set_browser_content(self._avisos_browser, texts.get('avisos'), texts.get('info_not_available_text', self.info_not_available_text))
            self.tabs.setTabText(3, texts['show_notices_text'])

            self._set_browser_content(self._privacidade_browser, texts.get('Privacy_Policy'), texts.get('info_not_available_text', self.info_not_available_text))
            self.tabs.setTabText(4, texts['show_privacy_policy_text'])

            self._set_browser_content(self._release_notes_browser, texts.get('release_notes'), texts.get('info_not_available_text', self.info_not_available_text))
            self.tabs.setTabText(5, texts['show_release_notes_text'])

            self.ok_button.setText(texts['ok_text'])

            self._show_labels = [
                texts['show_history_text'],
                texts['show_details_text'],
                texts['show_licenses_text'],
                texts['show_notices_text'],
                texts['show_privacy_policy_text'],
                texts['show_release_notes_text']
            ]

            self._hide_labels = [
                texts['hide_history_text'],
                texts['hide_details_text'],
                texts['hide_licenses_text'],
                texts['hide_notices_text'],
                texts['hide_privacy_policy_text'],
                texts['hide_release_notes_text']
            ]

            self._update_tab_labels(self.tabs.currentIndex())

        except Exception as e:
            logger.error(f"Erro ao retraduzir dialog sobre: {e}", exc_info=True)

        try:
            self.fixed_label.setOpenExternalLinks(True)

        except Exception:
            pass
