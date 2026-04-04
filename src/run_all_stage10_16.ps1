param(
    [ValidateSet("fail-fast", "ladder", "verify")]
    [string]$Mode = "fail-fast",
    [int[]]$Stages = @(10, 11, 12, 13, 14, 15, 16),
    [string]$PythonExe = "python",
    [switch]$IncludeLabs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Invoke-StageScript {
    param(
        [int]$Stage,
        [string]$Mode,
        [string]$PythonExe,
        [bool]$IncludeLabs
    )

    $stageDir = Join-Path $scriptDir ("stage-" + $Stage)
    if (-not (Test-Path $stageDir)) {
        throw "Missing stage directory: $stageDir"
    }

    if ($Mode -eq "fail-fast") {
        $target = Join-Path $stageDir ("run_all_stage" + $Stage + ".ps1")
        if (-not (Test-Path $target)) { throw "Missing runner: $target" }
        Write-Host "`n=== Stage ${Stage}: fail-fast ===" -ForegroundColor Cyan
        & powershell -ExecutionPolicy Bypass -File $target -PythonExe $PythonExe
        if ($LASTEXITCODE -ne 0) { throw "Stage $Stage fail-fast runner failed." }
        return
    }

    if ($Mode -eq "ladder") {
        $target = Join-Path $stageDir ("run_ladder_stage" + $Stage + ".ps1")
        if (-not (Test-Path $target)) { throw "Missing ladder runner: $target" }
        Write-Host "`n=== Stage ${Stage}: ladder ===" -ForegroundColor Cyan
        if ($IncludeLabs) {
            & powershell -ExecutionPolicy Bypass -File $target -PythonExe $PythonExe -IncludeLabs
        } else {
            & powershell -ExecutionPolicy Bypass -File $target -PythonExe $PythonExe
        }
        if ($LASTEXITCODE -ne 0) { throw "Stage $Stage ladder runner failed." }
        return
    }

    if ($Mode -eq "verify") {
        $target = Join-Path $stageDir ("verify_stage" + $Stage + "_outputs.ps1")
        if (-not (Test-Path $target)) { throw "Missing verify script: $target" }
        Write-Host "`n=== Stage ${Stage}: verify ===" -ForegroundColor Cyan
        & powershell -ExecutionPolicy Bypass -File $target
        if ($LASTEXITCODE -ne 0) { throw "Stage $Stage output verification failed." }
        return
    }

    throw "Unsupported mode: $Mode"
}

Write-Host "Cross-stage orchestrator" -ForegroundColor Green
Write-Host "Mode      : $Mode"
Write-Host "Stages    : $($Stages -join ', ')"
Write-Host "PythonExe : $PythonExe"
Write-Host "Labs      : $IncludeLabs"

foreach ($stage in $Stages) {
    Invoke-StageScript -Stage $stage -Mode $Mode -PythonExe $PythonExe -IncludeLabs:$IncludeLabs
}

Write-Host "`nAll requested stages completed successfully." -ForegroundColor Green

