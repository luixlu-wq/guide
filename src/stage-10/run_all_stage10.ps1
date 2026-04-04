param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_integration_flow_intermediate.py",
    "topic01_data_contracts_intermediate.py",
    "topic02_feature_pipeline_intermediate.py",
    "topic03_ml_prediction_intermediate.py",
    "topic04_retrieval_context_intermediate.py",
    "topic05_llm_reasoning_intermediate.py",
    "topic06_api_serving_intermediate.py",
    "topic07_evaluation_regression_intermediate.py",
    "topic08_ops_release_intermediate.py",
    "lab01_end_to_end_baseline.py"
)

Write-Host "Stage 10 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 10 fail-fast scripts completed successfully." -ForegroundColor Green

