param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_pytorch_cuda_rag_intermediate.py",
    "topic01_ingestion_chunking_intermediate.py",
    "topic02_embeddings_index_intermediate.py",
    "topic03_retrieval_rerank_intermediate.py",
    "topic04_grounding_intermediate.py",
    "topic05_eval_metrics_intermediate.py",
    "topic06_ops_cost_latency_intermediate.py",
    "lab01_pdf_qa_rag.py"
)

Write-Host "Stage 7 fail-fast runner" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"

foreach ($name in $scripts) {
    $path = Join-Path $scriptDir $name
    if (-not (Test-Path $path)) {
        throw "Missing script: $path"
    }

    Write-Host ""
    Write-Host ">>> Running $name" -ForegroundColor Yellow
    & $PythonExe $path
    if ($LASTEXITCODE -ne 0) {
        throw "Failed: $name (exit code $LASTEXITCODE)"
    }
}

Write-Host ""
Write-Host "All Stage 7 fail-fast scripts completed successfully." -ForegroundColor Green
