param(
    [string]$PythonExe = "python",
    [switch]$IncludeGpu
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic01_numpy_vectorization.py",
    "topic02_numpy_shape_broadcasting.py",
    "topic03_pandas_load_inspect.py",
    "topic04_pandas_clean_transform.py",
    "topic05_feature_engineering_time_series.py",
    "topic06_matplotlib_data_debugging.py",
    "topic07_sklearn_split_preprocess.py",
    "topic08_sklearn_pipeline_leakage.py",
    "topic09_stage2_end_to_end_pipeline.py"
)

if ($IncludeGpu) {
    $scripts += "topic10_pytorch_cuda_bridge.py"
}

Write-Host "Stage 2 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 2 scripts completed successfully." -ForegroundColor Green
