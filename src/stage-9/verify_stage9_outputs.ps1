Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"

if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    "lab1_api_contract.json",
    "lab1_latency_breakdown.csv",
    "lab1_boundary_checklist.md",
    "lab2_qdrant_collection_stats.json",
    "lab2_retrieval_quality.csv",
    "lab2_failure_cases.md",
    "lab3_serving_latency_compare.csv",
    "lab3_throughput_compare.csv",
    "lab3_operational_tradeoffs.md",
    "lab4_load_test_summary.csv",
    "lab4_incident_timeline.md",
    "lab4_fix_options_comparison.csv",
    "lab4_verification_rerun.csv",
    "lab5_baseline_architecture.md",
    "lab5_improved_architecture.md",
    "lab5_metrics_comparison.csv",
    "lab5_solution_options.csv",
    "lab5_incident_or_risk_log.md",
    "lab5_rollback_plan.md",
    "lab5_production_readiness.md"
)

$missing = New-Object System.Collections.Generic.List[string]
$empty = New-Object System.Collections.Generic.List[string]

foreach ($name in $required) {
    $path = Join-Path $resultsDir $name
    if (-not (Test-Path $path)) {
        $missing.Add($name)
        continue
    }

    $item = Get-Item $path
    if ($item.Length -eq 0) {
        $empty.Add($name)
    }
}

Write-Host ""
Write-Host "Stage 9 output verification" -ForegroundColor Cyan
Write-Host "Results directory: $resultsDir"
Write-Host "Required files: $($required.Count)"

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing files ($($missing.Count)):" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
}

if ($empty.Count -gt 0) {
    Write-Host ""
    Write-Host "Empty files ($($empty.Count)):" -ForegroundColor Yellow
    $empty | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
}

if ($missing.Count -eq 0 -and $empty.Count -eq 0) {
    Write-Host ""
    Write-Host "PASS: all required Stage 9 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "FAIL: output verification failed. Regenerate missing/empty artifacts and rerun." -ForegroundColor Red
exit 1

