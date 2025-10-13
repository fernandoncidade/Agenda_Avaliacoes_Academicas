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

Versão: v0.0.1.0 — 09 de Outubro de 2025  
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
- Política de Privacidade: `assets/PRIVACY_POLICY/Privacy_Policy_pt_BR.txt`.

## Licença, notices e terceiros

- Projeto licenciado sob MIT — veja `LICENSE`.
- Componentes de terceiros e avisos: `assets/NOTICES/NOTICE_pt_BR.txt`.
- Dependências: `requirements.txt`.

## Contrato comercial (quando aplicável)

- Para usos comerciais e redistribuição consultar: `assets/CLC/CLC_pt_BR - Compression Manager.txt`.

## Sobre / Histórico

- Informações e motivação do projeto: `assets/ABOUT/ABOUT_pt_BR.txt` e `assets/ABOUT/History_APP_pt_BR.txt`.
- Release notes: `assets/RELEASE/RELEASE NOTES_pt_BR.txt`.

## Contribuição e suporte

- Relatos de bugs, sugestões e pull requests: abrir issue no repositório.
- Contato / suporte: Fernando Nillsson Cidade — linceu_lighthouse@outlook.com

--- 

Pequena nota: esta é a primeira versão pública (v0.0.1.0). O foco foi estabilidade e simplicidade; futuras versões trarão filtros avançados, importação/exportação adicionais e melhorias de usabilidade.

**Total de downloads acumulados:**  
![GitHub all releases](https://img.shields.io/github/downloads/fernandoncidade/Agenda_Avaliacoes_Academicas/total?label=Downloads%20totais%20(Agenda%20Avaliações%20Acadêmicas))


</details>

<h2 id="enus">🇺🇸 English (US)</h2>

<details>
<summary>Click to expand the README in English</summary>

# ACADEMIC ASSESSMENTS SCHEDULE

Version: v0.0.1.0 — October 9, 2025  
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
- Privacy Policy: `assets/PRIVACY_POLICY/Privacy_Policy_pt_BR.txt`.

## License, notices and third parties

- Project licensed under MIT — see `LICENSE`.
- Third-party components and notices: `assets/NOTICES/NOTICE_pt_BR.txt`.
- Dependencies: `requirements.txt`.

## Commercial agreement (when applicable)

- For commercial use and redistribution consult: `assets/CLC/CLC_pt_BR - Compression Manager.txt`.

## About / History

- Project information and motivation: `assets/ABOUT/ABOUT_pt_BR.txt` and `assets/ABOUT/History_APP_pt_BR.txt`.
- Release notes: `assets/RELEASE/RELEASE NOTES_pt_BR.txt`.

## Contribution and support

- Bug reports, suggestions and pull requests: open an issue on the repository.
- Contact / support: Fernando Nillsson Cidade — linceu_lighthouse@outlook.com

--- 

Small note: this is the first public version (v0.0.1.0). The focus was stability and simplicity; future releases will bring advanced filters, additional import/export and usability improvements.

**Total cumulative downloads:**  
![GitHub all releases](https://img.shields.io/github/downloads/fernandoncidade/Agenda_Avaliacoes_Academicas/total?label=Total%20Downloads%20(Agenda%20Avaliações%20Acadêmicas))

</details>
