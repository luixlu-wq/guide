param(
    [string]$PythonExe = "python",
    [switch]$IncludeGpuBridge
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:LOKY_MAX_CPU_COUNT = "1"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic01a_linear_regression_simple.py",
    "topic01_linear_regression.py",
    "topic01c_linear_regression_advanced.py",
    "topic02a_logistic_regression_simple.py",
    "topic02_logistic_regression.py",
    "topic02c_logistic_regression_advanced.py",
    "topic03a_decision_tree_simple.py",
    "topic03_decision_tree_depth.py",
    "topic03c_decision_tree_advanced.py",
    "topic04a_random_forest_simple.py",
    "topic04_random_forest_baseline.py",
    "topic04c_random_forest_advanced.py",
    "topic05a_svm_simple.py",
    "topic05_svm_tuning.py",
    "topic05c_svm_advanced.py",
    "topic06a_kmeans_simple.py",
    "topic06_kmeans_silhouette.py",
    "topic06c_kmeans_advanced.py"
)

if ($IncludeGpuBridge) {
    $scripts += @(
        "topic09a_pytorch_cuda_simple.py",
        "topic09_pytorch_cuda_bridge.py",
        "topic09c_pytorch_cuda_advanced.py"
    )
}

Write-Host "Stage 3 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include GPU bridge ladder: $IncludeGpuBridge"

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
Write-Host "All Stage 3 ladder scripts completed successfully." -ForegroundColor Green
