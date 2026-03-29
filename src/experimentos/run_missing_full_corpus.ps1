# Ejecuta los experimentos que aun NO tienen resultado, usando el corpus completo (sin muestreo).
# Ejecutar desde la raiz del repo: .\src\experimentos\run_missing_full_corpus.ps1
#
# Corpus generado: corpus_repo\corpus_v1. Corpus real (para exp 07): data\real_validation_corpus.

$ErrorActionPreference = "Stop"

$corpusRoot = "corpus_repo\corpus_v1"
$realCorpus = "data\real_validation_corpus"

Write-Host "Corpus (generado): $corpusRoot"
Write-Host "Corpus real (exp 07): $realCorpus"
Write-Host ""

python run_missing_experiments.py --corpus_root $corpusRoot --real_corpus $realCorpus --full_corpus
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Listo."
