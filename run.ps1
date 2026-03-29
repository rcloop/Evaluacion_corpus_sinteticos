# Run a command from the repository root. Works in PowerShell 5.x and 7+.
# Usage: .\run.ps1 <command> [args...]
# Example: .\run.ps1 python -u src/experimentos/sesgos/01_name_gender_distribution.py --corpus_root corpus_repo/corpus_v1

$ErrorActionPreference = "Stop"
$RepoRoot = $PSScriptRoot
Push-Location $RepoRoot
try {
    if ($args.Count -eq 0) {
        Write-Host "Usage: .\run.ps1 <command> [args...]"
        exit 1
    }
    $cmd = $args[0]
    $cmdArgs = @($args[1..($args.Length - 1)])
    & $cmd @cmdArgs
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
