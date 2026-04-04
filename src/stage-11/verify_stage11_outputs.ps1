Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"

if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    "lab1_serving_latency_compare.csv",
    "lab1_serving_throughput_compare.csv",
    "lab1_serving_tradeoffs.md",
    "throughput_vs_latency_batch_profile.csv",
    "lab2_gpu_profile_baseline.csv",
    "lab2_gpu_profile_improved.csv",
    "lab2_gpu_tuning_report.md",
    "fp4_throughput_quality_tradeoff.csv",
    "hardware_saturation_profile.jsonl",
    "wsl_io_before_after.csv",
    "lab3_vector_scale_metrics.csv",
    "lab3_retrieval_quality.csv",
    "lab3_vector_ops_findings.md",
    "vector_recall_vs_latency_matrix.csv",
    "qdrant_persistence_recovery.md",
    "lab4_incident_baseline.csv",
    "lab4_solution_options.csv",
    "lab4_verification_rerun.csv",
    "lab4_release_decision.md",
    "circuit_breaker_events.jsonl",
    "sse_ttft_metrics.csv",
    "sse_disconnect_recovery.md",
    "otel_trace_path_validation.md",
    "wsl_network_trace_check.md",
    "incident_postmortem_infra.md",
    "local_stack_boot_report.md",
    "service_health_snapshot.json",
    "release_readiness.json"
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
Write-Host "Stage 11 output verification" -ForegroundColor Cyan
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
    Write-Host "PASS: all required Stage 11 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "FAIL: output verification failed. Regenerate missing/empty artifacts and rerun." -ForegroundColor Red
exit 1
