Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"
if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    'lab1_architecture_options.csv',
    'lab1_tradeoff_matrix.csv',
    'lab1_decision_record.md',
    'lab2_incident_timeline.csv',
    'lab2_actions_and_owners.csv',
    'lab2_postmortem.md',
    'lab3_audit_checklist.csv',
    'lab3_risk_register.csv',
    'lab3_audit_recommendation.md',
    'lab4_portfolio_index.md',
    'lab4_case_study_summary.md',
    'lab4_capability_matrix.csv',
    'stage16/system_mastery_rubric.md',
    'stage16/dependency_risk_map.md',
    'stage16/lab02_silent_sev1_timeline.csv',
    'stage16/lab02_kill_switch_evidence.md',
    'stage16/compute_efficiency_report.csv',
    'stage16/power_perf_curve.csv',
    'stage16/mastery_scorecard.csv',
    'stage16/lab04_portfolio_evidence_pack.md',
    'stage16/lab04_final_y_statement.md'
)

$missing = New-Object System.Collections.Generic.List[string]
$empty = New-Object System.Collections.Generic.List[string]
foreach ($name in $required) {
    $path = Join-Path $resultsDir $name
    if (-not (Test-Path $path)) { $missing.Add($name); continue }
    if ((Get-Item $path).Length -eq 0) { $empty.Add($name) }
}

Write-Host ""
Write-Host "Stage 16 output verification" -ForegroundColor Cyan
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
    Write-Host "PASS: all required Stage 16 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}
Write-Host ""
Write-Host "FAIL: output verification failed." -ForegroundColor Red
exit 1
