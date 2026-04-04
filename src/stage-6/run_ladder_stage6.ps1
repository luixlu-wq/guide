param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_pytorch_cuda_agent_simple.py",
    "topic00_pytorch_cuda_agent_intermediate.py",
    "topic00c_pytorch_cuda_agent_advanced.py",
    "topic01a_workflow_first_simple.py",
    "topic01_workflow_vs_agent_intermediate.py",
    "topic01c_multi_step_agent_advanced.py",
    "topic02a_tool_schema_simple.py",
    "topic02_tool_validation_intermediate.py",
    "topic02c_tool_failure_recovery_advanced.py",
    "topic03a_memory_basics_simple.py",
    "topic03_memory_retrieval_intermediate.py",
    "topic03c_memory_policy_advanced.py",
    "topic04a_guardrails_simple.py",
    "topic04_hitl_intermediate.py",
    "topic04c_policy_gated_actions_advanced.py",
    "topic05a_trace_basics_simple.py",
    "topic05_eval_metrics_intermediate.py",
    "topic05c_regression_suite_advanced.py",
    "topic06_industry_patterns.py",
    "topic07a_mcp_tooling_simple.py",
    "topic07_protocol_interop_intermediate.py",
    "topic07c_a2a_collaboration_advanced.py",
    "topic08a_budget_controls_simple.py",
    "topic08_latency_cost_optimization_intermediate.py",
    "topic08c_slo_regression_gate_advanced.py",
    "topic09a_prompt_injection_defense_simple.py",
    "topic09_policy_and_permissions_intermediate.py",
    "topic09c_incident_response_advanced.py"
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        "lab01_support_triage_agent.py",
        "lab02_finance_research_agent.py",
        "lab03_multi_agent_ops_assistant.py",
        "lab04_secure_agent_operations.py"
    )
}

Write-Host "Stage 6 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
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
Write-Host "All Stage 6 ladder scripts completed successfully." -ForegroundColor Green
