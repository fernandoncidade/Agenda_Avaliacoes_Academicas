<!-- Multilanguage README.md for Agenda_Avaliacoes_Academicas -->

<p align="center">
  <b>Selecione o idioma / Select language:</b><br>
  <a href="#ptbr">🇧🇷 Português (BR)</a> |
  <a href="#enus">🇺🇸 English (US)</a>
</p>

---

<h2 id="ptbr">🇧🇷 Português (BR)</h2>

<details>
<summary>Clique para expandir o README em português</summary>

# AGENDA DE AVALIAÇÕES ACADÊMICAS

Versão: v2026.4.24.0<br>
Autor: Fernando Nillsson Cidade

## Visão geral

Agenda de Avaliações Acadêmicas é um utilitário gráfico leve para Windows (Python + PySide6) que consolida, organiza e apresenta datas de atividades avaliativas (provas, trabalhos, apresentações etc.) em uma visão cronológica única. Oferece exportação para PDF, destaque por cores, edição em lote e interface multilíngue (pt_BR / en_US).

## Funcionalidades principais

- Registro de atividades com campos: curso, ementa, semestre, disciplina, turma, tipo de avaliação, sequência e data.
- Visão cronológica consolidada e ordenação automática por data.
- Destaque por cores para identificação rápida.
- Exportação para PDF (ReportLab).
- Edição individual e em lote; exclusão selecionada.
- Persistência de preferências e dados locais em JSON (%APPDATA% no Windows).
- Interface multilíngue com troca em tempo de execução.
- Janela "Sobre" com histórico, licenças, notices e política de privacidade integrados.
- Preparado para empacotamento como executável Windows (PyInstaller).

## Requisitos

- Python 3.x (para desenvolvimento)
- Dependências listadas em `requirements.txt` (PySide6, ReportLab, etc.)

Instalar dependências:
```bash
pip install -r requirements.txt
```

## Como executar (desenvolvimento)

```bash
python main.py
```

Observação: o executável criado para distribuição inclui dependências empacotadas — o usuário final NÃO precisa instalar Python.

## Empacotamento (exemplo)

Exemplo simples com PyInstaller:
```bash
pyinstaller --noconfirm --onefile --windowed main.py
```
Ajuste hooks e arquivos de dados conforme necessário (traduções, assets, LICENSES, NOTICE, Privacy Policy).

## Testes rápidos / verificação

- Abra o aplicativo.
- Registre algumas atividades completas (preencha todos os campos).
- Confirme ordenação cronológica e destaque por cores.
- Exporte para PDF e verifique o arquivo gerado.
- Troque o idioma para English e verifique traduções.

## Privacidade e armazenamento

- Todos os dados do usuário são mantidos localmente; o executável padrão não envia telemetria automática.
- Política de Privacidade: `source/assets/PRIVACY_POLICY/Privacy_Policy_pt_BR.txt`.

## Licença, notices e terceiros

- Projeto licenciado sob GNU LGPL v3 — veja `LICENSE`.
- Componentes de terceiros e avisos: `source/assets/NOTICES/NOTICE_pt_BR.txt`.
- Dependências principais: Qt 6, SQLite, plugins Qt e runtimes aplicáveis à build.

## Nota legal

Fernando Nillsson Cidade é o autor, mantenedor e titular originário deste projeto, bem como das marcas, nomes e distribuições oficiais associadas ao software. Distribuições oficiais, suporte oficial e ofertas comerciais realizadas em nome do projeto dependem de sua autorização.

A GNU LGPL v3 não concede, por si só, direitos de uso de marca. Este aviso não reduz nem substitui os direitos concedidos pela licença deste projeto e pelas licenças de terceiros distribuídas com ele. Terceiros podem instalar, usar, estudar, modificar e redistribuir o software nos termos da licença aplicável, devendo preservar os avisos legais e cumprir as obrigações da distribuição. Quanto aos componentes do framework Qt licenciados sob a GNU LGPL v3, terceiros podem substituir os arquivos correspondentes do framework, conforme essa licença: <https://www.gnu.org/licenses/lgpl-3.0.html.en>.

## Termos comerciais opcionais

- O uso, estudo, modificação e redistribuição do software seguem a GNU LGPL v3 e não exigem licença comercial separada.
- Para suporte oficial, serviços de customização, uso de marca/nome em distribuições oficiais ou publicação oficial em lojas digitais, consulte: `source/assets/CLC/CLC_pt_BR.txt`.

## Sobre / Histórico

- Informações e motivação do projeto: `source/assets/ABOUT/ABOUT_pt_BR.txt` e `source/assets/ABOUT/History_APP_pt_BR.txt`.
- Release notes: `source/assets/RELEASE/RELEASE NOTES_pt_BR.txt`.

## Contribuição e suporte

- Relatos de bugs, sugestões e pull requests: abrir issue no repositório.
- Contato / suporte: Fernando Nillsson Cidade — linceu_lighthouse@outlook.com

--- 

Pequena nota: esta é a primeira versão pública (v2026.4.24.0). O foco foi estabilidade e simplicidade; futuras versões trarão filtros avançados, importação/exportação adicionais e melhorias de usabilidade.

--- 

</details>

<h2 id="enus">🇺🇸 English (US)</h2>

<details>
<summary>Click to expand the README in English</summary>

# ACADEMIC ASSESSMENTS SCHEDULE

Version: v2026.4.24.0<br>
Author: Fernando Nillsson Cidade

## Overview

Academic Assessments Schedule is a lightweight graphical utility for Windows (Python + PySide6) that consolidates, organizes and presents dates of evaluative activities (exams, assignments, presentations, etc.) in a single chronological view. It offers PDF export, color highlighting, batch editing and a multilingual interface (pt_BR / en_US).

## Main features

- Record activities with fields: course, syllabus, semester, subject, class, assessment type, sequence and date.
- Consolidated chronological view and automatic sorting by date.
- Color highlighting for quick identification.
- PDF export (ReportLab).
- Individual and batch editing; selected deletion.
- Persistence of preferences and local data in JSON (%APPDATA% on Windows).
- Multilingual interface with runtime switching.
- "About" window with integrated history, licenses, notices and privacy policy.
- Prepared for packaging as a Windows executable (PyInstaller).

## Requirements

- Python 3.x (for development)
- Dependencies listed in `requirements.txt` (PySide6, ReportLab, etc.)

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to run (development)

```bash
python main.py
```

Note: the executable built for distribution includes packaged dependencies — the end user DOES NOT need to install Python.

## Packaging (example)

Simple example with PyInstaller:
```bash
pyinstaller --noconfirm --onefile --windowed main.py
```
Adjust hooks and data files as needed (translations, assets, LICENSES, NOTICE, Privacy Policy).

## Quick tests / verification

- Open the application.
- Register some complete activities (fill all fields).
- Confirm chronological sorting and color highlighting.
- Export to PDF and check the generated file.
- Switch the language to English and verify translations.

## Privacy and storage

- All user data is kept locally; the default executable does not send automatic telemetry.
- Privacy Policy: `source/assets/PRIVACY_POLICY/Privacy_Policy_en_US.txt`.

## License, notices and third parties

- Project licensed under GNU LGPL v3 — see `LICENSE`.
- Third-party components and notices: `source/assets/NOTICES/NOTICE_en_US.txt`.
- Main dependencies: Qt 6, SQLite, Qt plugins and build-specific runtime components.

## Legal notice

Fernando Nillsson Cidade is the author, maintainer and original right holder of this project, as well as of the trademarks, names and official distributions associated with the software. Official distributions, official support and commercial offers made in the name of the project depend on his authorization.

The GNU LGPL v3 does not, by itself, grant trademark rights. This notice does not reduce or replace the rights granted by this project's license and by third-party licenses distributed with it. Third parties may install, use, study, modify and redistribute the software under the applicable license, provided they preserve the legal notices and comply with the distribution obligations. With respect to Qt framework components licensed under the GNU LGPL v3, third parties may replace the corresponding framework files in accordance with that license: <https://www.gnu.org/licenses/lgpl-3.0.html.en>.

## Optional commercial terms

- Use, study, modification and redistribution of the software are governed by the GNU LGPL v3 and do not require a separate commercial license.
- For official support, customization services, trademark/name use in official distributions or official publication in digital stores, consult: `source/assets/CLC/CLC_en_US.txt`.

## About / History

- Project information and motivation: `source/assets/ABOUT/ABOUT_en_US.txt` and `source/assets/ABOUT/History_APP_en_US.txt`.
- Release notes: `source/assets/RELEASE/RELEASE NOTES_en_US.txt`.

## Contribution and support

- Bug reports, suggestions and pull requests: open an issue on the repository.
- Contact / support: Fernando Nillsson Cidade — linceu_lighthouse@outlook.com

--- 

Small note: this is the first public version (v2026.4.24.0). The focus was stability and simplicity; future releases will bring advanced filters, additional import/export and usability improvements.

--- 

</details>
