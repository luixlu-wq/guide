param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_infra_basics_intermediate.py",
    "topic01_serving_patterns_intermediate.py",
    "topic02_gpu_cuda_ops_intermediate.py",
    "topic03_vector_db_ops_intermediate.py",
    "topic04_distributed_decisions_intermediate.py",
    "topic05_monitoring_alerting_intermediate.py",
    "topic06_capacity_cost_intermediate.py",
    "topic07_incident_response_intermediate.py",
    "lab01_serving_benchmark.py"
)

Write-Host "Stage 11 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 11 fail-fast scripts completed successfully." -ForegroundColor Green

