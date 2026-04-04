param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs,
    [switch]$IncludeQdrant
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_pytorch_cuda_tuning_simple.py",
    "topic00_pytorch_cuda_tuning_intermediate.py",
    "topic00c_pytorch_cuda_tuning_advanced.py",
    "topic01a_dataset_schema_simple.py",
    "topic01_dataset_quality_intermediate.py",
    "topic01c_data_governance_advanced.py",
    "topic02a_sft_baseline_simple.py",
    "topic02_sft_intermediate.py",
    "topic02c_sft_eval_advanced.py",
    "topic03a_lora_simple.py",
    "topic03_lora_intermediate.py",
    "topic03c_lora_rank_sweep_advanced.py",
    "topic04a_qlora_simple.py",
    "topic04_qlora_intermediate.py",
    "topic04c_qlora_memory_tradeoff_advanced.py",
    "topic05a_distill_simple.py",
    "topic05_distill_intermediate.py",
    "topic05c_distill_eval_advanced.py",
    "topic06a_prompt_vs_tune_simple.py",
    "topic06_tune_vs_rag_intermediate.py",
    "topic06c_hybrid_strategy_advanced.py",
    "topic07a_eval_basics_simple.py",
    "topic07_eval_regression_intermediate.py",
    "topic07c_promotion_gate_advanced.py",
    "topic08a_model_registry_simple.py",
    "topic08_ops_observability_intermediate.py",
    "topic08c_canary_rollback_advanced.py"
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        "lab01_instruction_tuning_baseline.py",
        "lab02_lora_qlora_comparison.py",
        "lab03_distillation_tradeoff_lab.py",
        "lab04_finetune_project_baseline_to_production.py"
    )
}

if ($IncludeQdrant -and $IncludeLabs) {
    $scripts = $scripts + @(
        "lab05_finetune_vs_rag_vs_hybrid_qdrant.py"
    )
}

Write-Host "Stage 8 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include labs: $IncludeLabs"
Write-Host "Include Qdrant: $IncludeQdrant"

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
Write-Host "All Stage 8 ladder scripts completed successfully." -ForegroundColor Green
