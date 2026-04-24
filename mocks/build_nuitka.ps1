[CmdletBinding()]
param(
    [string]$OutputDir = 'D:\MISCELANEAS\Nuitka\Agenda_Avaliacoes_Academicas'
)

$ErrorActionPreference = 'Stop'

$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).ProviderPath
$iconPath = Join-Path $projectRoot 'source\assets\icones\ReviewsManager.ico'
$assetsPath = Join-Path $projectRoot 'source\assets'
$translationsPath = Join-Path $projectRoot 'source\language\translations'

if (-not (Test-Path -LiteralPath $iconPath)) {
    throw "Icone nao encontrado: $iconPath"
}

if (-not (Test-Path -LiteralPath $assetsPath)) {
    throw "Diretorio de assets nao encontrado: $assetsPath"
}

if (-not (Test-Path -LiteralPath $translationsPath)) {
    throw "Diretorio de traducoes nao encontrado: $translationsPath"
}

$nuitkaArgs = @(
    '-m', 'nuitka',
    '--standalone',
    '--follow-imports',
    '--enable-plugin=pyside6',
    '--enable-plugin=pylint-warnings',
    '--enable-plugin=anti-bloat',
    '--msvc=latest',
    '--include-package=PySide6.QtCore',
    '--include-package=PySide6.QtGui',
    '--include-package=PySide6.QtWidgets',
    '--include-data-dir=source\assets=assets',
    '--include-data-dir=source\language\translations=language\translations',
    '--windows-icon-from-ico=source\assets\icones\ReviewsManager.ico',
    "--output-dir=$OutputDir",
    '--output-filename=Agenda_Avaliacoes_Academicas',
    '--windows-console-mode=disable',
    '--show-progress',
    '--show-memory',
    '--assume-yes-for-downloads',
    'main.py'
)

Push-Location -LiteralPath $projectRoot
try {
    python @nuitkaArgs
}
finally {
    Pop-Location
}
