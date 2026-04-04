Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"

if (-not (Test-Path $resultsDir)) {
    Write-Host "Missing results directory: $resultsDir" -ForegroundColor Red
    exit 1
}

$required = @(
    "lab1_pattern_metrics.csv",
    "lab1_tradeoff_matrix.csv",
    "lab1_pattern_summary.md",
    "lab2_failure_cases.csv",
    "lab2_solution_options.csv",
    "lab2_verification_rerun.csv",
    "lab3_decision_scores.csv",
    "lab3_adr.md",
    "adr_scorecard_with_thresholds.csv",
    "architecture_decision_y_statement.md",
    "lab4_baseline_metrics.csv",
    "lab4_improved_metrics.csv",
    "lab4_metrics_comparison.csv",
    "lab4_release_decision.md",
    "lab4_rollback_plan.md",
    "release_gate_report.md",
    "rollback_simulation.md",
    "agent_card_registry.json",
    "a2a_handoff_trace.jsonl",
    "mcp_tool_contracts.md",
    "nvfp4_throughput_quality.csv",
    "prefix_cache_latency_profile.csv",
    "agent_loop_latency_report.md",
    "indirect_injection_case_log.jsonl",
    "unbounded_consumption_guard.csv",
    "owasp_llm_v2_redteam_report.md",
    "geojson_schema_guard_failures.csv",
    "loop_breaker_events.jsonl",
    "coordinate_projection_validation_report.md",
    "mobile_latency_guard_report.md"
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
Write-Host "Stage 12 output verification" -ForegroundColor Cyan
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
    Write-Host "PASS: all required Stage 12 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "FAIL: output verification failed. Regenerate missing/empty artifacts and rerun." -ForegroundColor Red
exit 1
