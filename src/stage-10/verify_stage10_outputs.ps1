Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"

if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    "lab1_layer_metrics.csv",
    "lab1_system_metrics.csv",
    "lab1_baseline_outputs.jsonl",
    "lab2_contract_checks.csv",
    "lab2_contract_failures.md",
    "lab2_failure_cases.csv",
    "lab2_contract_fix_report.md",
    "lab3_incident_baseline.csv",
    "lab3_solution_options.csv",
    "lab3_verification_rerun.csv",
    "lab3_verification_notes.md",
    "lab3_decision.md",
    "lab4_baseline_outputs.jsonl",
    "lab4_improved_outputs.jsonl",
    "lab4_layer_metrics.csv",
    "lab4_solution_options.csv",
    "lab4_metrics_comparison.csv",
    "lab4_verification_report.md",
    "lab4_production_readiness.md",
    "release_decision.md",
    "canary_eval_report.md",
    "trace_sample_analysis.jsonl",
    "otel_trace_contract_report.md",
    "throughput_vllm_vs_trt.csv",
    "hardware_saturation_log.jsonl",
    "hardware_quantization_report.md",
    "production_eval_store.jsonl",
    "hallucination_drift_log.jsonl",
    "judge_alignment_report.md",
    "circuit_breaker_incident_log.jsonl",
    "incident_postmortem_drill.md",
    "drift_telemetry_report.csv",
    "vector_drift_analysis.md",
    "rollback_drill.md"
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
Write-Host "Stage 10 output verification" -ForegroundColor Cyan
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
    Write-Host "PASS: all required Stage 10 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "FAIL: output verification failed. Regenerate artifacts and rerun." -ForegroundColor Red
exit 1
