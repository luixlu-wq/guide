param(
    [string]$PythonExe = "python",
    [switch]$IncludeGpu
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvDir = Join-Path $scriptDir ".venv"
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

Write-Host ""
Write-Host "Pre-flight checks" -ForegroundColor Cyan
if (Test-Path $venvDir) {
    Write-Host "  .venv found: $venvDir"
} else {
    Write-Warning ".venv not found under stage folder ($venvDir). Ensure dependencies are installed in the selected Python environment."
}

& $PythonExe --version
if ($LASTEXITCODE -ne 0) {
    throw "Python executable check failed: $PythonExe"
}

if ($IncludeGpu) {
    Write-Host "  GPU pre-flight: checking nvidia-smi..."
    $nvidiaSmi = Get-Command "nvidia-smi" -ErrorAction SilentlyContinue
    if (-not $nvidiaSmi) {
        throw "IncludeGpu was set but nvidia-smi is not available in PATH."
    }

    & nvidia-smi | Select-Object -First 15
    if ($LASTEXITCODE -ne 0) {
        throw "nvidia-smi failed. Verify NVIDIA driver/CUDA runtime before running GPU topic."
    }
}

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
