param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    'topic00a_competency_matrix_simple.py',
    'topic00_competency_matrix_intermediate.py',
    'topic00c_competency_matrix_advanced.py',
    'topic01a_architecture_reviews_simple.py',
    'topic01_architecture_reviews_intermediate.py',
    'topic01c_architecture_reviews_advanced.py',
    'topic02a_incident_command_simple.py',
    'topic02_incident_command_intermediate.py',
    'topic02c_incident_command_advanced.py',
    'topic03a_quality_security_simple.py',
    'topic03_quality_security_intermediate.py',
    'topic03c_quality_security_advanced.py',
    'topic04a_team_workflows_simple.py',
    'topic04_team_workflows_intermediate.py',
    'topic04c_team_workflows_advanced.py',
    'topic05a_portfolio_evidence_simple.py',
    'topic05_portfolio_evidence_intermediate.py',
    'topic05c_portfolio_evidence_advanced.py',
    'topic06a_continuous_improvement_simple.py',
    'topic06_continuous_improvement_intermediate.py',
    'topic06c_continuous_improvement_advanced.py'
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        'lab01_architecture_review_simulation.py',
        'lab02_incident_command_drill.py',
        'lab03_quality_governance_audit.py',
        'lab04_industry_project_portfolio_pack.py'
    )
}

Write-Host "Stage 16 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
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
Write-Host "All Stage 16 ladder scripts completed successfully." -ForegroundColor Green
