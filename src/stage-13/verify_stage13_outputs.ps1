Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"
if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    'lab1_capstone_baseline_metrics.csv',
    'lab1_capstone_layer_outputs.jsonl',
    'lab1_capstone_contract_status.csv',
    'lab2_solution_options.csv',
    'lab2_before_after_delta.csv',
    'lab2_improvement_decision.md',
    'lab3_incident_timeline.csv',
    'lab3_root_cause_analysis.md',
    'lab3_verification_rerun.csv',
    'lab4_release_gate_checklist.csv',
    'lab4_release_decision.md',
    'lab4_rollback_plan.md'
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
    if ($item.Length -eq 0) { $empty.Add($name) }
}

Write-Host ""
Write-Host "Stage 13 output verification" -ForegroundColor Cyan
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
    Write-Host "PASS: all required Stage 13 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}
Write-Host ""
Write-Host "FAIL: output verification failed." -ForegroundColor Red
exit 1
