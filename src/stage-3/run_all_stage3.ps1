param(
    [string]$PythonExe = "python",
    [switch]$IncludeGpu
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:LOKY_MAX_CPU_COUNT = "1"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic01_linear_regression.py",
    "topic02_logistic_regression.py",
    "topic03_decision_tree_depth.py",
    "topic04_random_forest_baseline.py",
    "topic05_svm_tuning.py",
    "topic06_kmeans_silhouette.py",
    "topic07_fair_model_comparison.py",
    "topic08_failure_modes_overfit_leakage.py"
)

if ($IncludeGpu) {
    $scripts += "topic09_pytorch_cuda_bridge.py"
}

Write-Host "Stage 3 fail-fast runner" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include GPU track: $IncludeGpu"

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
Write-Host "All Stage 3 scripts completed successfully." -ForegroundColor Green
