param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    'topic00_trading_system_basics_intermediate.py',
    'topic01_signal_quality_intermediate.py',
    'topic02_risk_engine_intermediate.py',
    'topic03_portfolio_optimizer_intermediate.py',
    'topic04_execution_sim_intermediate.py',
    'topic05_stress_test_intermediate.py',
    'topic06_ops_governance_intermediate.py',
    'lab01_multi_asset_baseline.py'
)

Write-Host "Stage 14 fail-fast runner" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"

foreach ($name in $scripts) {
    $path = Join-Path $scriptDir $name
    if (-not (Test-Path $path)) { throw "Missing script: $path" }
    Write-Host ""
    Write-Host ">>> Running $name" -ForegroundColor Yellow
    & $PythonExe $path
    if ($LASTEXITCODE -ne 0) { throw "Failed: $name (exit code $LASTEXITCODE)" }
}

Write-Host ""
Write-Host "All Stage 14 fail-fast scripts completed successfully." -ForegroundColor Green
