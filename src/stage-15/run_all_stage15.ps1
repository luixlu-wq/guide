param(
    [string]$PythonExe = "python",
    [string]$Lab = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    'topic00_failure_definition_intermediate.py',
    'topic01_evidence_collection_intermediate.py',
    'topic02_experiment_design_intermediate.py',
    'topic03_ml_debug_intermediate.py',
    'topic04_llm_debug_intermediate.py',
    'topic05_rag_debug_intermediate.py',
    'topic06_verification_gates_intermediate.py',
    'topic07_postmortem_intermediate.py',
    'lab01_ml_failure_diagnosis.py'
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

Write-Host "Stage 15 fail-fast runner" -ForegroundColor Cyan
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
Write-Host "All Stage 15 fail-fast scripts completed successfully." -ForegroundColor Green
