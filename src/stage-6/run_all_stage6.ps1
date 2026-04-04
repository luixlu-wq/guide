param(
    [string]$PythonExe = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00_pytorch_cuda_agent_intermediate.py",
    "topic01_workflow_vs_agent_intermediate.py",
    "topic02_tool_validation_intermediate.py",
    "topic03_memory_retrieval_intermediate.py",
    "topic04_hitl_intermediate.py",
    "topic05_eval_metrics_intermediate.py",
    "topic06_industry_patterns.py",
    "topic07_protocol_interop_intermediate.py",
    "topic08_latency_cost_optimization_intermediate.py",
    "topic09_policy_and_permissions_intermediate.py",
    "lab01_support_triage_agent.py"
)

Write-Host "Stage 6 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 6 fail-fast scripts completed successfully." -ForegroundColor Green
