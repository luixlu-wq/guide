param(
    [string]$PythonExe = "python",
    [ValidateSet("quick", "full")]
    [string]$Preset = "full",
    [switch]$IncludeGpu
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:STAGE4_PRESET = $Preset

$scripts = @(
    "topic01_loop_anatomy.py",
    "topic02_mlp_intermediate.py",
    "topic03_cnn_intermediate.py",
    "topic04_rnn_intermediate.py",
    "topic05_transformer_intermediate.py",
    "topic07_failure_modes.py",
    "topic08_project_baseline.py"
)

if ($IncludeGpu) {
    $scripts += "topic06_cuda_intermediate.py"
}

Write-Host "Stage 4 fail-fast runner" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Preset          : $Preset"
Write-Host "Include GPU track: $IncludeGpu"

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
Write-Host "All Stage 4 scripts completed successfully." -ForegroundColor Green
