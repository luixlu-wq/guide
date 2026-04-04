param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_system_flow_intermediate.py",
    "topic01_qdrant_retrieval_intermediate.py",
    "topic02_vllm_serving_intermediate.py",
    "topic03_queue_backpressure_intermediate.py",
    "topic04_pytorch_amp_intermediate.py",
    "topic05_metrics_tracing_intermediate.py",
    "topic06_retry_timeout_intermediate.py",
    "topic07_k8s_deploy_intermediate.py",
    "topic08_tradeoff_analysis_intermediate.py",
    "lab01_modular_ai_backend.py"
)

Write-Host "Stage 9 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 9 fail-fast scripts completed successfully." -ForegroundColor Green

