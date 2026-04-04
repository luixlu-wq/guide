param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_integration_flow_simple.py",
    "topic00_integration_flow_intermediate.py",
    "topic00c_integration_flow_advanced.py",
    "topic01a_data_contracts_simple.py",
    "topic01_data_contracts_intermediate.py",
    "topic01c_data_contracts_advanced.py",
    "topic02a_feature_pipeline_simple.py",
    "topic02_feature_pipeline_intermediate.py",
    "topic02c_feature_pipeline_advanced.py",
    "topic03a_ml_prediction_simple.py",
    "topic03_ml_prediction_intermediate.py",
    "topic03c_ml_prediction_advanced.py",
    "topic04a_retrieval_context_simple.py",
    "topic04_retrieval_context_intermediate.py",
    "topic04c_retrieval_context_advanced.py",
    "topic05a_llm_reasoning_simple.py",
    "topic05_llm_reasoning_intermediate.py",
    "topic05c_llm_reasoning_advanced.py",
    "topic06a_api_serving_simple.py",
    "topic06_api_serving_intermediate.py",
    "topic06c_api_serving_advanced.py",
    "topic07a_evaluation_regression_simple.py",
    "topic07_evaluation_regression_intermediate.py",
    "topic07c_evaluation_regression_advanced.py",
    "topic08a_ops_release_simple.py",
    "topic08_ops_release_intermediate.py",
    "topic08c_ops_release_advanced.py"
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        "lab01_end_to_end_baseline.py",
        "lab02_pipeline_contract_validation.py",
        "lab03_incident_diagnosis_and_fix.py",
        "lab04_baseline_to_production_integration.py",
        "lab05_observability_genai_and_trace_contract.py",
        "lab06_hardware_saturation_and_quantization.py",
        "lab07_eval_store_and_feedback_loop.py",
        "lab08_circuit_breaker_incident_response.py",
        "lab09_vector_drift_and_index_refresh.py",
        "lab10_model_regression_rollback_drill.py"
    )
}

Write-Host "Stage 10 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
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
Write-Host "All Stage 10 ladder scripts completed successfully." -ForegroundColor Green
