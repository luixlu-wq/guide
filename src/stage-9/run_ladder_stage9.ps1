param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_system_flow_simple.py",
    "topic00_system_flow_intermediate.py",
    "topic00c_system_flow_advanced.py",
    "topic01a_qdrant_ingest_simple.py",
    "topic01_qdrant_retrieval_intermediate.py",
    "topic01c_qdrant_failure_diagnostics_advanced.py",
    "topic02a_ollama_serving_simple.py",
    "topic02_vllm_serving_intermediate.py",
    "topic02c_ray_serve_orchestration_advanced.py",
    "topic03a_latency_budget_simple.py",
    "topic03_queue_backpressure_intermediate.py",
    "topic03c_autoscaling_policy_advanced.py",
    "topic04a_pytorch_device_basics_simple.py",
    "topic04_pytorch_amp_intermediate.py",
    "topic04c_cuda_oom_recovery_advanced.py",
    "topic05a_structured_logging_simple.py",
    "topic05_metrics_tracing_intermediate.py",
    "topic05c_incident_triage_advanced.py",
    "topic06a_input_validation_simple.py",
    "topic06_retry_timeout_intermediate.py",
    "topic06c_sla_slo_error_budget_advanced.py",
    "topic07a_single_node_compose_simple.py",
    "topic07_k8s_deploy_intermediate.py",
    "topic07c_canary_rollback_advanced.py",
    "topic08a_decision_matrix_simple.py",
    "topic08_tradeoff_analysis_intermediate.py",
    "topic08c_architecture_review_board_advanced.py"
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        "lab01_modular_ai_backend.py",
        "lab02_vector_retrieval_service_qdrant.py",
        "lab03_serving_stack_comparison.py",
        "lab04_scaling_and_observability_incident_lab.py",
        "lab05_architecture_project_baseline_to_production.py"
    )
}

Write-Host "Stage 9 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
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
Write-Host "All Stage 9 ladder scripts completed successfully." -ForegroundColor Green

