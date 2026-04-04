param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    'topic00a_trading_system_basics_simple.py',
    'topic00_trading_system_basics_intermediate.py',
    'topic00c_trading_system_basics_advanced.py',
    'topic01a_signal_quality_simple.py',
    'topic01_signal_quality_intermediate.py',
    'topic01c_signal_quality_advanced.py',
    'topic02a_risk_engine_simple.py',
    'topic02_risk_engine_intermediate.py',
    'topic02c_risk_engine_advanced.py',
    'topic03a_portfolio_optimizer_simple.py',
    'topic03_portfolio_optimizer_intermediate.py',
    'topic03c_portfolio_optimizer_advanced.py',
    'topic04a_execution_sim_simple.py',
    'topic04_execution_sim_intermediate.py',
    'topic04c_execution_sim_advanced.py',
    'topic05a_stress_test_simple.py',
    'topic05_stress_test_intermediate.py',
    'topic05c_stress_test_advanced.py',
    'topic06a_ops_governance_simple.py',
    'topic06_ops_governance_intermediate.py',
    'topic06c_ops_governance_advanced.py'
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        'lab01_multi_asset_baseline.py',
        'lab02_risk_engine_improvement.py',
        'lab03_execution_slippage_impact.py',
        'lab04_stress_test_and_recovery.py'
    )
}

Write-Host "Stage 14 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include labs: $IncludeLabs"

foreach ($name in $scripts) {
    $path = Join-Path $scriptDir $name
    if (-not (Test-Path $path)) { throw "Missing script: $path" }
    Write-Host ""
    Write-Host ">>> Running $name" -ForegroundColor Yellow
    & $PythonExe $path
    if ($LASTEXITCODE -ne 0) { throw "Failed: $name (exit code $LASTEXITCODE)" }
}

Write-Host ""
Write-Host "All Stage 14 ladder scripts completed successfully." -ForegroundColor Green
