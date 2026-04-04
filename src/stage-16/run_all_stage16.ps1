param(
    [string]$PythonExe = "python",
    [string]$Lab = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    'topic00_competency_matrix_intermediate.py',
    'topic01_architecture_reviews_intermediate.py',
    'topic02_incident_command_intermediate.py',
    'topic03_quality_security_intermediate.py',
    'topic04_team_workflows_intermediate.py',
    'topic05_portfolio_evidence_intermediate.py',
    'topic06_continuous_improvement_intermediate.py',
    'lab01_architecture_review_simulation.py'
)

if ($Lab -ne "") {
    $candidate = "$Lab.py"
    if (Test-Path (Join-Path $scriptDir $candidate)) {
        $scripts = @($candidate)
    }
    elseif (Test-Path (Join-Path $scriptDir $Lab)) {
        $scripts = @($Lab)
    }
    else {
        throw "Requested lab script not found: $Lab"
    }
}

Write-Host "Stage 16 fail-fast runner" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
if ($Lab -ne "") { Write-Host "Selected lab   : $Lab" }

foreach ($name in $scripts) {
    $path = Join-Path $scriptDir $name
    if (-not (Test-Path $path)) { throw "Missing script: $path" }
    Write-Host ""
    Write-Host ">>> Running $name" -ForegroundColor Yellow
    & $PythonExe $path
    if ($LASTEXITCODE -ne 0) { throw "Failed: $name (exit code $LASTEXITCODE)" }
}

Write-Host ""
Write-Host "All Stage 16 fail-fast scripts completed successfully." -ForegroundColor Green
