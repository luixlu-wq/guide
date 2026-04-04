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
    "lab1_base_outputs.jsonl",
    "lab1_tuned_outputs.jsonl",
    "lab1_metrics_comparison.csv",
    "lab1_error_cases.md",
    "lab2_lora_metrics.csv",
    "lab2_qlora_metrics.csv",
    "lab2_memory_latency_report.md",
    "lab3_teacher_outputs.jsonl",
    "lab3_student_outputs.jsonl",
    "lab3_distillation_report.md",
    "lab4_project_baseline_outputs.jsonl",
    "lab4_project_improved_outputs.jsonl",
    "lab4_solution_options.csv",
    "lab4_metrics_comparison.csv",
    "lab4_verification_report.md",
    "lab4_production_readiness.md"
)

if ($IncludeQdrant) {
    $required += @(
        "lab5_compare_prompt_rag_tune.csv",
        "lab5_qdrant_retrieval_metrics.csv",
        "lab5_final_decision.md"
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
Write-Host "Stage 8 output verification" -ForegroundColor Cyan
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
    Write-Host "PASS: all required Stage 8 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "FAIL: output verification failed. Regenerate missing/empty artifacts and rerun." -ForegroundColor Red
exit 1
