param(
    [switch]$IncludeQdrant
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"

if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    "lab1_outputs.jsonl",
    "lab1_retrieval_metrics.csv",
    "lab1_grounding_audit.md",
    "lab2_outputs.jsonl",
    "lab2_policy_violations.csv",
    "lab2_fix_log.md",
    "lab3_retrieval_comparison.csv",
    "lab3_error_cases.md",
    "lab3_before_after_summary.md",
    "lab4_sync_log.md",
    "lab4_acl_validation.csv",
    "lab4_slo_report.csv",
    "lab4_incident_postmortem.md",
    "lab6_project_baseline_outputs.jsonl",
    "lab6_project_improved_outputs.jsonl",
    "lab6_project_solution_options.csv",
    "lab6_project_metrics_comparison.csv",
    "lab6_project_verification_report.md",
    "lab6_project_production_readiness.md"
)

if ($IncludeQdrant) {
    $required += @(
        "lab5_qdrant_outputs.jsonl",
        "lab5_qdrant_metrics.csv",
        "lab5_qdrant_acl_validation.csv",
        "lab5_qdrant_runbook.md"
    )
}

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
Write-Host "Stage 7 output verification" -ForegroundColor Cyan
Write-Host "Results directory: $resultsDir"
Write-Host "Include Qdrant files: $IncludeQdrant"
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
    Write-Host "PASS: all required Stage 7 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "FAIL: output verification failed. Regenerate missing/empty artifacts and rerun." -ForegroundColor Red
exit 1

