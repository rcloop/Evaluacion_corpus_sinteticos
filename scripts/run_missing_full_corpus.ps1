# Run experiments that still lack results (full corpus, no sampling).
# Can be invoked from anywhere; working directory is set to the repo root.
#
# Corpus generado: corpus_repo\corpus_v1. Corpus real (exp 07): corpus_repo\real_validation_corpus.

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path $PSScriptRoot -Parent
Push-Location $RepoRoot
try {
    $corpusRoot = "corpus_repo\corpus_v1"
    $realCorpus = "corpus_repo\real_validation_corpus"

    Write-Host "Corpus (generado): $corpusRoot"
    Write-Host "Corpus real (exp 07): $realCorpus"
    Write-Host ""

    python scripts/run_missing_experiments.py --corpus_root $corpusRoot --real_corpus $realCorpus --full_corpus
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "Listo."
} finally {
    Pop-Location
}
