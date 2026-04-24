[CmdletBinding(SupportsShouldProcess = $true)]
param()

$ErrorActionPreference = 'Stop'

$workspaceRoot = 'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas'
$resolvedWorkspaceRoot = (Resolve-Path -LiteralPath $workspaceRoot).ProviderPath.TrimEnd('\')

$pycachePaths = @(
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\BancoDeDados\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\BancoDeDados\DicionariosListasBancoDeDados\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\GerenciamentoAtividades\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\GerenciamentoAtividades\GerenciadorAtividades\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\GerenciamentoInterfaceGrafica\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\GerenciamentoInterfaceGrafica\GerenciadorInterfaceGrafica\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\language\__pycache__',
    'C:\Users\ferna\DEV\Python\Agenda_Avaliacoes_Academicas\source\utils\__pycache__'
)

foreach ($path in $pycachePaths) {
    if (-not (Test-Path -LiteralPath $path)) {
        Write-Host "Ignorado (nao existe): $path"
        continue
    }

    $resolvedPath = (Resolve-Path -LiteralPath $path).ProviderPath

    if (-not $resolvedPath.StartsWith($resolvedWorkspaceRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        Write-Warning "Ignorado fora do workspace: $resolvedPath"
        continue
    }

    if ($PSCmdlet.ShouldProcess($resolvedPath, 'Remover diretorio __pycache__')) {
        Remove-Item -LiteralPath $resolvedPath -Recurse -Force
        Write-Host "Removido: $resolvedPath"
    }
}

Write-Host 'Limpeza concluida.'
