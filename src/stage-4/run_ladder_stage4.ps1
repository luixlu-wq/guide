param(
    [string]$PythonExe = "python",
    [ValidateSet("quick", "full")]
    [string]$Preset = "full",
    [switch]$IncludeGpuBridge
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:STAGE4_PRESET = $Preset

$scripts = @(
    "topic01a_loop_anatomy_simple.py",
    "topic01_loop_anatomy.py",
    "topic01c_loop_anatomy_advanced.py",
    "topic02a_mlp_simple.py",
    "topic02_mlp_intermediate.py",
    "topic02c_mlp_advanced.py",
    "topic03a_cnn_simple.py",
    "topic03_cnn_intermediate.py",
    "topic03c_cnn_advanced.py",
    "topic04a_rnn_simple.py",
    "topic04_rnn_intermediate.py",
    "topic04c_rnn_advanced.py",
    "topic05a_transformer_simple.py",
    "topic05_transformer_intermediate.py",
    "topic05c_transformer_advanced.py"
)

if ($IncludeGpuBridge) {
    $scripts += @(
        "topic06a_cuda_simple.py",
        "topic06_cuda_intermediate.py",
        "topic06c_cuda_amp_advanced.py"
    )
}

Write-Host "Stage 4 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Preset           : $Preset"
Write-Host "Include GPU bridge ladder: $IncludeGpuBridge"

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
Write-Host "All Stage 4 ladder scripts completed successfully." -ForegroundColor Green
