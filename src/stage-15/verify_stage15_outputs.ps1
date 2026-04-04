Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"
if (-not (Test-Path $resultsDir)) { Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red; exit 1 }

$required = @(
    'lab1_ml_baseline_metrics.csv',
    'lab1_ml_failure_analysis.md',
    'lab1_ml_verification_rerun.csv',
    'lab2_prompt_cases.csv',
    'lab2_prompt_options.csv',
    'lab2_prompt_verification.csv',
    'lab3_retrieval_baseline.csv',
    'lab3_retrieval_options.csv',
    'lab3_retrieval_verification.csv',
    'lab4_solution_compare.csv',
    'lab4_verification_rerun.csv',
    'lab4_decision_record.md'
)

$missing = New-Object System.Collections.Generic.List[string]
$empty = New-Object System.Collections.Generic.List[string]
foreach ($name in $required) {
    $path = Join-Path $resultsDir $name
    if (-not (Test-Path $path)) { $missing.Add($name); continue }
    if ((Get-Item $path).Length -eq 0) { $empty.Add($name) }
}

Write-Host ""; Write-Host "Stage 15 output verification" -ForegroundColor Cyan
Write-Host "Results directory: $resultsDir"
Write-Host "Required files: $($required.Count)"
if ($missing.Count -gt 0) { Write-Host ""; Write-Host "Missing files ($($missing.Count)):" -ForegroundColor Red; $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red } }
if ($empty.Count -gt 0) { Write-Host ""; Write-Host "Empty files ($($empty.Count)):" -ForegroundColor Yellow; $empty | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow } }
if ($missing.Count -eq 0 -and $empty.Count -eq 0) { Write-Host ""; Write-Host "PASS: all required Stage 15 output files exist and are non-empty." -ForegroundColor Green; exit 0 }
Write-Host ""; Write-Host "FAIL: output verification failed." -ForegroundColor Red
exit 1
