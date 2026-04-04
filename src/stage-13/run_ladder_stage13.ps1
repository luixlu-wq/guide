param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    'topic00a_capstone_scope_simple.py',
    'topic00_capstone_scope_intermediate.py',
    'topic00c_capstone_scope_advanced.py',
    'topic01a_contracts_validation_simple.py',
    'topic01_contracts_validation_intermediate.py',
    'topic01c_contracts_validation_advanced.py',
    'topic02a_integration_pipeline_simple.py',
    'topic02_integration_pipeline_intermediate.py',
    'topic02c_integration_pipeline_advanced.py',
    'topic03a_evaluation_pack_simple.py',
    'topic03_evaluation_pack_intermediate.py',
    'topic03c_evaluation_pack_advanced.py',
    'topic04a_incident_workflow_simple.py',
    'topic04_incident_workflow_intermediate.py',
    'topic04c_incident_workflow_advanced.py',
    'topic05a_release_readiness_simple.py',
    'topic05_release_readiness_intermediate.py',
    'topic05c_release_readiness_advanced.py'
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        'lab01_capstone_baseline.py',
        'lab02_capstone_improvement_cycle.py',
        'lab03_capstone_incident_response.py',
        'lab04_capstone_production_readiness.py'
    )
}

Write-Host "Stage 13 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
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
Write-Host "All Stage 13 ladder scripts completed successfully." -ForegroundColor Green
