param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    'topic00a_failure_definition_simple.py',
    'topic00_failure_definition_intermediate.py',
    'topic00c_failure_definition_advanced.py',
    'topic01a_evidence_collection_simple.py',
    'topic01_evidence_collection_intermediate.py',
    'topic01c_evidence_collection_advanced.py',
    'topic02a_experiment_design_simple.py',
    'topic02_experiment_design_intermediate.py',
    'topic02c_experiment_design_advanced.py',
    'topic03a_ml_debug_simple.py',
    'topic03_ml_debug_intermediate.py',
    'topic03c_ml_debug_advanced.py',
    'topic04a_llm_debug_simple.py',
    'topic04_llm_debug_intermediate.py',
    'topic04c_llm_debug_advanced.py',
    'topic05a_rag_debug_simple.py',
    'topic05_rag_debug_intermediate.py',
    'topic05c_rag_debug_advanced.py',
    'topic06a_verification_gates_simple.py',
    'topic06_verification_gates_intermediate.py',
    'topic06c_verification_gates_advanced.py',
    'topic07a_postmortem_simple.py',
    'topic07_postmortem_intermediate.py',
    'topic07c_postmortem_advanced.py'
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        'lab01_ml_failure_diagnosis.py',
        'lab02_llm_prompt_regression.py',
        'lab03_rag_retrieval_failure.py',
        'lab04_option_compare_and_verify.py'
    )
}

Write-Host "Stage 15 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include labs: $IncludeLabs"

foreach ($name in $scripts) {
    $path = Join-Path $scriptDir $name
    if (-not (Test-Path $path)) { throw "Missing script: $path" }
    Write-Host ""
    Write-Host ">>> Running $name" -ForegroundColor Yellow
    & $PythonExe $path
    if ($LASTEXITCODE -ne 0) { throw "Failed: $name (exit code $LASTEXITCODE)" }
}

Write-Host ""
Write-Host "All Stage 15 ladder scripts completed successfully." -ForegroundColor Green
