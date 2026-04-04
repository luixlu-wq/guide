param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_architecture_decision_intermediate.py",
    "topic01_llm_app_pattern_intermediate.py",
    "topic02_rag_pattern_intermediate.py",
    "topic03_agent_pattern_intermediate.py",
    "topic04_multi_agent_pattern_intermediate.py",
    "topic05_pattern_comparison_intermediate.py",
    "topic06_safety_governance_intermediate.py",
    "topic07_release_rollback_intermediate.py",
    "lab01_pattern_baseline_compare.py",
    "lab02_rag_vs_agent_failure_drill.py",
    "lab03_architecture_decision_record.py",
    "lab04_pattern_to_production.py",
    "lab05_a2a_mcp_interoperability.py",
    "lab06_blackwell_nvfp4_prefix_caching.py",
    "lab07_owasp_llm_v2_redteam.py",
    "lab08_gis_projection_and_loop_breaker.py"
)

Write-Host "Stage 12 fail-fast runner" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"

foreach ($name in $scripts) {
    $path = Join-Path $scriptDir $name
    if (-not (Test-Path $path)) {
        throw "Missing script: $path"
    }
    Write-Host ""
    Write-Host ">>> Running $name" -ForegroundColor Yellow
    & $PythonExe $path
    if ($LASTEXITCODE -ne 0) {
        throw "Failed: $name (exit code $LASTEXITCODE)"
    }
}

Write-Host ""
Write-Host "All Stage 12 fail-fast scripts completed successfully." -ForegroundColor Green
