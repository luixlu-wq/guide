Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"
if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    'lab1_multi_asset_baseline_metrics.csv',
    'lab1_signal_summary.csv',
    'lab1_portfolio_weights.csv',
    'lab2_risk_before_after.csv',
    'lab2_constraint_changes.csv',
    'lab2_risk_decision.md',
    'lab3_execution_cost_profile.csv',
    'lab3_slippage_scenarios.csv',
    'lab3_execution_findings.md',
    'lab4_stress_results.csv',
    'lab4_recovery_actions.csv',
    'lab4_release_recommendation.md'
)

$missing = New-Object System.Collections.Generic.List[string]
$empty = New-Object System.Collections.Generic.List[string]
foreach ($name in $required) {
    $path = Join-Path $resultsDir $name
    if (-not (Test-Path $path)) { $missing.Add($name); continue }
    if ((Get-Item $path).Length -eq 0) { $empty.Add($name) }
}

Write-Host ""
Write-Host "Stage 14 output verification" -ForegroundColor Cyan
Write-Host "Results directory: $resultsDir"
Write-Host "Required files: $($required.Count)"

if ($missing.Count -gt 0) { Write-Host ""; Write-Host "Missing files ($($missing.Count)):" -ForegroundColor Red; $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red } }
if ($empty.Count -gt 0) { Write-Host ""; Write-Host "Empty files ($($empty.Count)):" -ForegroundColor Yellow; $empty | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow } }
if ($missing.Count -eq 0 -and $empty.Count -eq 0) { Write-Host ""; Write-Host "PASS: all required Stage 14 output files exist and are non-empty." -ForegroundColor Green; exit 0 }
Write-Host ""; Write-Host "FAIL: output verification failed." -ForegroundColor Red
exit 1
