param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_pytorch_cuda_tuning_intermediate.py",
    "topic01_dataset_quality_intermediate.py",
    "topic02_sft_intermediate.py",
    "topic03_lora_intermediate.py",
    "topic04_qlora_intermediate.py",
    "topic05_distill_intermediate.py",
    "topic06_tune_vs_rag_intermediate.py",
    "topic07_eval_regression_intermediate.py",
    "topic08_ops_observability_intermediate.py",
    "lab01_instruction_tuning_baseline.py"
)

Write-Host "Stage 8 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 8 fail-fast scripts completed successfully." -ForegroundColor Green
