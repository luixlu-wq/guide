param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_infra_basics_simple.py",
    "topic00_infra_basics_intermediate.py",
    "topic00c_infra_basics_advanced.py",
    "topic01a_serving_patterns_simple.py",
    "topic01_serving_patterns_intermediate.py",
    "topic01c_serving_patterns_advanced.py",
    "topic02a_gpu_cuda_ops_simple.py",
    "topic02_gpu_cuda_ops_intermediate.py",
    "topic02c_gpu_cuda_ops_advanced.py",
    "topic03a_vector_db_ops_simple.py",
    "topic03_vector_db_ops_intermediate.py",
    "topic03c_vector_db_ops_advanced.py",
    "topic04a_distributed_decisions_simple.py",
    "topic04_distributed_decisions_intermediate.py",
    "topic04c_distributed_decisions_advanced.py",
    "topic05a_monitoring_alerting_simple.py",
    "topic05_monitoring_alerting_intermediate.py",
    "topic05c_monitoring_alerting_advanced.py",
    "topic06a_capacity_cost_simple.py",
    "topic06_capacity_cost_intermediate.py",
    "topic06c_capacity_cost_advanced.py",
    "topic07a_incident_response_simple.py",
    "topic07_incident_response_intermediate.py",
    "topic07c_incident_response_advanced.py"
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        "lab01_serving_benchmark.py",
        "lab02_gpu_utilization_tuning.py",
        "lab03_vector_db_scale_diagnostics.py",
        "lab04_infra_incident_recovery.py"
    )
}

Write-Host "Stage 11 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
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
Write-Host "All Stage 11 ladder scripts completed successfully." -ForegroundColor Green

