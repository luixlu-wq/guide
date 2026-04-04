param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_architecture_decision_simple.py",
    "topic00_architecture_decision_intermediate.py",
    "topic00c_architecture_decision_advanced.py",
    "topic01a_llm_app_pattern_simple.py",
    "topic01_llm_app_pattern_intermediate.py",
    "topic01c_llm_app_pattern_advanced.py",
    "topic02a_rag_pattern_simple.py",
    "topic02_rag_pattern_intermediate.py",
    "topic02c_rag_pattern_advanced.py",
    "topic03a_agent_pattern_simple.py",
    "topic03_agent_pattern_intermediate.py",
    "topic03c_agent_pattern_advanced.py",
    "topic04a_multi_agent_pattern_simple.py",
    "topic04_multi_agent_pattern_intermediate.py",
    "topic04c_multi_agent_pattern_advanced.py",
    "topic05a_pattern_comparison_simple.py",
    "topic05_pattern_comparison_intermediate.py",
    "topic05c_pattern_comparison_advanced.py",
    "topic06a_safety_governance_simple.py",
    "topic06_safety_governance_intermediate.py",
    "topic06c_safety_governance_advanced.py",
    "topic07a_release_rollback_simple.py",
    "topic07_release_rollback_intermediate.py",
    "topic07c_release_rollback_advanced.py"
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        "lab01_pattern_baseline_compare.py",
        "lab02_rag_vs_agent_failure_drill.py",
        "lab03_architecture_decision_record.py",
        "lab04_pattern_to_production.py",
        "lab05_a2a_mcp_interoperability.py",
        "lab06_blackwell_nvfp4_prefix_caching.py",
        "lab07_owasp_llm_v2_redteam.py",
        "lab08_gis_projection_and_loop_breaker.py"
    )
}

Write-Host "Stage 12 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include labs: $IncludeLabs"

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
Write-Host "All Stage 12 ladder scripts completed successfully." -ForegroundColor Green
