import sys
import re
from pathlib import Path

# garante que a raiz do projeto esteja no sys.path quando o script for executado diretamente
# (resolve o erro "ModuleNotFoundError: No module named 'source'")
_project_root = Path(__file__).resolve().parent.parent
_project_root_str = str(_project_root)
if _project_root_str not in sys.path:
    sys.path.insert(0, _project_root_str)

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                               QSpinBox, QComboBox, QPushButton, QTextEdit, QGroupBox, QFileDialog)
from PySide6.QtGui import QIcon
from source.utils.IconUtils import get_icon_path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

BASE_DIR = Path(__file__).resolve().parent.parent  # usar a raiz do projeto (um nível acima de tools)

FILES_REL = {
    "privacy_pt": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_pt_BR.txt",
    "privacy_en": Path("source") / "assets" / "PRIVACY_POLICY" / "Privacy_Policy_en_US.txt",
    "notice_pt": Path("source") / "assets" / "NOTICES" / "NOTICE_pt_BR.txt",
    "notice_en": Path("source") / "assets" / "NOTICES" / "NOTICE_en_US.txt",
    "eula_pt": Path("source") / "assets" / "EULA" / "EULA_pt_BR.txt",
    "eula_en": Path("source") / "assets" / "EULA" / "EULA_en_US.txt",
    "copyright_pt": Path("source") / "assets" / "COPYRIGHT" / "AVISO DE COPYRIGHT E MARCA REGISTRA_pt_BR.txt",
    "copyright_en": Path("source") / "assets" / "COPYRIGHT" / "COPYRIGHT AND TRADEMARK NOTICE_en_US.txt",
    "clc_pt": Path("source") / "assets" / "CLC" / "CLC_pt_BR.txt",
    "clc_en": Path("source") / "assets" / "CLC" / "CLC_en_US.txt",
    "about_pt": Path("source") / "assets" / "ABOUT" / "ABOUT_pt_BR.txt",
    "about_en": Path("source") / "assets" / "ABOUT" / "ABOUT_en_US.txt",
}

def get_files_for_base(base_dir: Path = BASE_DIR):
    files = {}
    base_dir = Path(base_dir)
    for key, rel_path in FILES_REL.items():
        candidate = base_dir / rel_path

        if candidate.exists():
            files[key] = candidate.resolve()
            continue

        rel_parts = rel_path.parts
        if rel_parts and rel_parts[0] == "source":
            alt = base_dir.joinpath(*rel_parts[1:])
            if alt.exists():
                files[key] = alt.resolve()
                continue

        files[key] = candidate.resolve()

    return files

EXPECTED = {
    "privacy_pt": [
        "Última atualização: 26 de novembro de 2025",
        "Versão: 2025.11.26.0",
    ],
    "privacy_en": [
        "Last updated: November 26, 2025",
        "Version: 2025.11.26.0",
    ],
    "notice_pt": [
        "Versão 2025.11.26.0, 26 de novembro de 2025",
    ],
    "notice_en": [
        "Version 2025.11.26.0, November 26, 2025",
    ],
    "eula_pt": [
        "Versão 2025.11.26.0, 26 de novembro de 2025",
    ],
    "eula_en": [
        "Version 2025.11.26.0, November 26, 2025",
    ],
    "copyright_pt": [
        "Versão 2025.11.26.0, 26 de novembro de 2025",
        "Copyright (C) 2025–2026 Fernando Nillsson Cidade. Todos os direitos reservados.",
    ],
    "copyright_en": [
        "Version 2025.11.26.0, November 26, 2025",
        "Copyright (C) 2025–2026 Fernando Nillsson Cidade. All rights reserved.",
    ],
    "clc_pt": [
        "Versão: 2025.11.26.0",
        "Data: 26 de novembro de 2025",
    ],
    "clc_en": [
        "Version: 2025.11.26.0",
        "Date: November 26, 2025",
    ],
    "about_pt": [
        "Versão: 2025.11.26.0",
    ],
    "about_en": [
        "Version: 2025.11.26.0",
    ],
}

PT_MONTHS = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
PT_MONTHS_LOWER = [m.lower() for m in PT_MONTHS]
EN_MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def read_file(path: Path):
    try:
        # tenta várias decodificações para evitar problemas com BOM/encodings diferentes
        try:
            return path.read_text(encoding="utf-8")

        except Exception:
            try:
                return path.read_text(encoding="utf-8-sig")

            except Exception:
                return path.read_text(encoding="latin-1")

    except Exception:
        return None

# padrões para extrair o que realmente está nos arquivos (não comparar com EXPECTED)
PATTERNS = {
    "privacy_pt": [
        r'^(Versão:\s*.*)$',
        r'^(Última atualização:\s*.*)$'
    ],
    "privacy_en": [
        r'^(Version:\s*.*)$',
        r'^(Last updated:\s*.*)$'
    ],
    "notice_pt": [
        r'^(Versão.*)$'
    ],
    "notice_en": [
        r'^(Version.*)$'
    ],
    "eula_pt": [
        r'^(Versão.*)$'
    ],
    "eula_en": [
        r'^(Version.*)$'
    ],
    "copyright_pt": [
        r'^(Versão.*)$',
        r'^(Copyright.*)$'
    ],
    "copyright_en": [
        r'^(Version.*)$',
        r'^(Copyright.*)$'
    ],
    "clc_pt": [
        r'^(Versão:\s*.*)$',
        r'^(Data:\s*.*)$'
    ],
    "clc_en": [
        r'^(Version:\s*.*)$',
        r'^(Date:\s*.*)$'
    ],
    "about_pt": [
        r'^(Versão:\s*.*)$'
    ],
    "about_en": [
        r'^(Version:\s*.*)$'
    ],
}

def check_expected_lines(base_dir: Path = BASE_DIR):
    status = {}
    files = get_files_for_base(base_dir)
    for key, path in files.items():
        txt = read_file(path)
        if txt is None:
            status[key] = {"exists": False, "found": [], "missing": []}
            continue

        found = []
        missing = []

        # para cada padrão associado àquele arquivo, procurar a linha correspondente
        patterns = PATTERNS.get(key, [])
        for pat in patterns:
            m = re.search(pat, txt, flags=re.MULTILINE)
            if m:
                found.append(m.group(1).strip())

            else:
                missing.append(pat)

        # se não houver padrões definidos, devolve as 3 primeiras linhas do arquivo como fallback
        if not patterns:
            lines = [l.rstrip("\r\n") for l in txt.splitlines()]
            found = lines[:3] if lines else []
            missing = []

        status[key] = {"exists": True, "found": found, "missing": missing}

    return status

def replace_file_content(path: Path, new_text: str):
    try:
        path.write_text(new_text, encoding="utf-8")
        return True, ""

    except Exception as e:
        return False, str(e)

def apply_updates(pt_version, pt_day, pt_month_index, pt_year, en_version, en_day, en_month_index, en_year, base_dir: Path = BASE_DIR):
    results = []
    files = get_files_for_base(base_dir)
    pt_month_name = PT_MONTHS_LOWER[pt_month_index]
    pt_date = f"{pt_day} de {pt_month_name} de {pt_year}"
    en_month_name = EN_MONTHS[en_month_index]
    en_date = f"{en_month_name} {en_day}, {en_year}"

    for key, path in files.items():
        txt = read_file(path)
        if txt is None:
            results.append((key, False, "arquivo inexistente"))
            continue

        original = txt
        new_txt = txt

        try:
            if key == "privacy_pt":
                new_txt = re.sub(r'^(Versão:\s*).*$',lambda m: m.group(1) + pt_version, new_txt, flags=re.MULTILINE)
                new_txt = re.sub(r'^(Última atualização:\s*).*$',lambda m: m.group(1) + pt_date, new_txt, flags=re.MULTILINE)

            elif key == "privacy_en":
                new_txt = re.sub(r'^(Version:\s*).*$',lambda m: m.group(1) + en_version, new_txt, flags=re.MULTILINE)
                new_txt = re.sub(r'^(Last updated:\s*).*$',lambda m: m.group(1) + en_date, new_txt, flags=re.MULTILINE)

            elif key in ("notice_pt", "eula_pt", "copyright_pt"):
                new_txt = re.sub(r'^(Versão\s*)([\d\.]+)\s*,\s*.*$',f"Versão {pt_version}, {pt_date}", new_txt, flags=re.MULTILINE)

            elif key in ("notice_en", "eula_en", "copyright_en"):
                new_txt = re.sub(r'^(Version\s*)([\d\.]+)\s*,\s*.*$',f"Version {en_version}, {en_date}", new_txt, flags=re.MULTILINE)

            elif key == "clc_pt":
                new_txt = re.sub(r'^(Versão:\s*).*$',lambda m: m.group(1) + pt_version, new_txt, flags=re.MULTILINE)
                new_txt = re.sub(r'^(Data:\s*).*$',lambda m: m.group(1) + pt_date, new_txt, flags=re.MULTILINE)

            elif key == "clc_en":
                new_txt = re.sub(r'^(Version:\s*).*$',lambda m: m.group(1) + en_version, new_txt, flags=re.MULTILINE)
                new_txt = re.sub(r'^(Date:\s*).*$',lambda m: m.group(1) + en_date, new_txt, flags=re.MULTILINE)

            elif key == "about_pt":
                new_txt = re.sub(r'^(Versão:\s*).*$',lambda m: m.group(1) + pt_version, new_txt, flags=re.MULTILINE)

            elif key == "about_en":
                new_txt = re.sub(r'^(Version:\s*).*$',lambda m: m.group(1) + en_version, new_txt, flags=re.MULTILINE)

            if new_txt != original:
                ok, err = replace_file_content(path, new_txt)
                if ok:
                    results.append((key, True, "atualizado"))

                else:
                    results.append((key, False, f"erro escrita: {err}"))

            else:
                results.append((key, False, "padrões não encontrados / sem alteração"))

        except Exception as e:
            results.append((key, False, f"erro: {e}"))

    return results


class VersionEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Versões / Datas - Lúmen (PT/EN)")
        self.resize(820, 520)

        try:
            icon_path = get_icon_path("autismo.ico")
            if icon_path:
                self.setWindowIcon(QIcon(icon_path))

        except Exception as e:
            logger.error(f"Erro ao carregar ícone da aplicação: {e}", exc_info=True)

        layout = QVBoxLayout(self)

        # pasta base selecionada (por padrão raiz do projeto)
        self.selected_base_dir = BASE_DIR

        # pasta de arquivos: seleção pelo usuário
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Pasta dos arquivos:"))
        self.folder_path = QLineEdit(str(self.selected_base_dir))
        self.folder_path.setReadOnly(True)
        folder_layout.addWidget(self.folder_path)
        self.select_folder_btn = QPushButton("Selecionar...")
        self.select_folder_btn.clicked.connect(self.on_select_folder)
        folder_layout.addWidget(self.select_folder_btn)
        layout.addLayout(folder_layout)

        # PT group
        pt_group = QGroupBox("Português (pt-BR)")
        pt_layout = QHBoxLayout()
        pt_group.setLayout(pt_layout)

        pt_layout.addWidget(QLabel("Versão:"))
        self.pt_version = QLineEdit("2025.11.26.0")
        pt_layout.addWidget(self.pt_version)

        pt_layout.addWidget(QLabel("Dia:"))
        self.pt_day = QSpinBox()
        self.pt_day.setRange(1, 31)
        self.pt_day.setValue(26)
        pt_layout.addWidget(self.pt_day)

        pt_layout.addWidget(QLabel("Mês:"))
        self.pt_month = QComboBox()
        self.pt_month.addItems(PT_MONTHS)
        self.pt_month.setCurrentIndex(10)  # Novembro
        pt_layout.addWidget(self.pt_month)

        pt_layout.addWidget(QLabel("Ano:"))
        self.pt_year = QSpinBox()
        self.pt_year.setRange(1900, 3000)
        self.pt_year.setValue(2025)
        pt_layout.addWidget(self.pt_year)

        layout.addWidget(pt_group)

        # EN group
        en_group = QGroupBox("English (en-US)")
        en_layout = QHBoxLayout()
        en_group.setLayout(en_layout)

        en_layout.addWidget(QLabel("Version:"))
        self.en_version = QLineEdit("2025.11.26.0")
        en_layout.addWidget(self.en_version)

        en_layout.addWidget(QLabel("Day:"))
        self.en_day = QSpinBox()
        self.en_day.setRange(1, 31)
        self.en_day.setValue(26)
        en_layout.addWidget(self.en_day)

        en_layout.addWidget(QLabel("Month:"))
        self.en_month = QComboBox()
        self.en_month.addItems(EN_MONTHS)
        self.en_month.setCurrentIndex(10)  # November
        en_layout.addWidget(self.en_month)

        en_layout.addWidget(QLabel("Year:"))
        self.en_year = QSpinBox()
        self.en_year.setRange(1900, 3000)
        self.en_year.setValue(2025)
        en_layout.addWidget(self.en_year)

        layout.addWidget(en_group)

        # Buttons and status
        btn_layout = QHBoxLayout()
        self.check_btn = QPushButton("🔍 Verificar arquivos")
        self.check_btn.clicked.connect(self.on_check)
        btn_layout.addWidget(self.check_btn)

        self.save_btn = QPushButton("💾 Salvar alterações")
        self.save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(self.save_btn)

        self.refresh_btn = QPushButton("🔄 Recarregar verificação")
        self.refresh_btn.clicked.connect(self.on_check)
        btn_layout.addWidget(self.refresh_btn)

        layout.addLayout(btn_layout)

        self.status = QTextEdit()
        self.status.setReadOnly(True)
        layout.addWidget(self.status)

        self.on_check()

    def on_select_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Selecione a pasta onde os arquivos estão", str(self.selected_base_dir))
        if dir_path:
            self.selected_base_dir = Path(dir_path)
            self.folder_path.setText(str(self.selected_base_dir))
            self.on_check()

    def on_check(self):
        # passa a pasta selecionada para a verificação
        status = check_expected_lines(self.selected_base_dir)
        lines = [f"Base: {self.selected_base_dir}"]
        for key, info in status.items():
            lines.append(f"{key}: file {'exists' if info['exists'] else 'missing'}")
            if info['exists']:
                if info["found"]:
                    lines.append("  found:")
                    for f in info["found"]:
                        lines.append(f"    - {f}")

                if info["missing"]:
                    lines.append("  missing:")
                    for m in info["missing"]:
                        lines.append(f"    - {m}")

            lines.append("")

        self.status.setPlainText("\n".join(lines))

    def on_save(self):
        pt_version = self.pt_version.text().strip()
        pt_day = self.pt_day.value()
        pt_month_index = self.pt_month.currentIndex()
        pt_year = self.pt_year.value()

        en_version = self.en_version.text().strip()
        en_day = self.en_day.value()
        en_month_index = self.en_month.currentIndex()
        en_year = self.en_year.value()

        # passa a pasta selecionada para a atualização
        results = apply_updates(pt_version, pt_day, pt_month_index, pt_year,
                                en_version, en_day, en_month_index, en_year,
                                base_dir=self.selected_base_dir)
        lines = ["Resultados:"]
        for key, ok, msg in results:
            lines.append(f"{key}: {'OK' if ok else 'FAIL'} - {msg}")

        self.status.setPlainText("\n".join(lines))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VersionEditor()
    w.show()
    sys.exit(app.exec())
