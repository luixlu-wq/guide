Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"
if (-not (Test-Path $resultsDir)) { Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red; exit 1 }

$required = @(
    'lab1_ml_baseline_metrics.csv',
    'lab1_ml_failure_analysis.md',
    'lab1_ml_verification_rerun.csv',
    'stage15/ml_failure_statement.md',
    'stage15/ml_root_cause.md',
    'stage15/icv_protocol_report.md',
    'stage15/lab01_wsl_cuda_contention_report.md',
    'stage15/lab01_gpu_telemetry_log.csv',
    'lab2_prompt_cases.csv',
    'lab2_prompt_options.csv',
    'lab2_prompt_verification.csv',
    'stage15/prompt_regression_table.csv',
    'stage15/prompt_fix_note.md',
    'stage15/lab02_prompt_regression.md',
    'lab3_retrieval_baseline.csv',
    'lab3_retrieval_options.csv',
    'lab3_retrieval_verification.csv',
    'stage15/retrieval_diagnostics.csv',
    'stage15/groundedness_delta.csv',
    'stage15/lab03_gis_boundary_failure_report.md',
    'stage15/lab03_projection_vs_topk_compare.csv',
    'lab4_solution_compare.csv',
    'lab4_verification_rerun.csv',
    'lab4_decision_record.md',
    'stage15/option_compare_table.csv',
    'stage15/final_decision.md',
    'stage15/lab04_option_compare_evidence.csv',
    'stage15/lab04_final_y_statement.md'
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
