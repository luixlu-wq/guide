param(
    [string]$PythonExe = "python",
    [switch]$IncludeGpu
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic01_supervised_learning.py",
    "topic02_unsupervised_learning.py",
    "topic03_features_vs_target.py",
    "topic04_cost_function.py",
    "topic05_gradient_descent.py",
    "topic06_training_vs_testing.py",
    "topic07_overfitting.py",
    "topic08_bias_variance.py",
    "topic09_validation_set.py",
    "topic10_feature_engineering.py",
    "topic11_regularization.py"
)

if ($IncludeGpu) {
    $scripts += "topic12_pytorch_cuda.py"
}

Write-Host "Stage 1 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 1 scripts completed successfully." -ForegroundColor Green
