param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_pytorch_cuda_intermediate.py",
    "topic01_multihead_attention.py",
    "topic01_tokenization_intermediate.py",
    "topic02_prompting_intermediate.py",
    "topic03_structured_output_intermediate.py",
    "topic04_rag_intermediate.py",
    "topic05_embeddings_intermediate.py",
    "topic07_prompt_eval_regression.py",
    "topic08_project_baseline.py"
)

Write-Host "Stage 5 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 5 scripts completed successfully." -ForegroundColor Green
