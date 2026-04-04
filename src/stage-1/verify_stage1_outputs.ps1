Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsDir = Join-Path $scriptDir "results"

$requiredInRoot = @(
    "topic05_loss_curve.png"
)

$requiredInResults = @(
    "pain_point_matrix.md",
    "before_after_metrics.csv",
    "verification_report.md",
    "decision_log.md",
    "reproducibility.md"
)

$missing = New-Object System.Collections.Generic.List[string]
$empty = New-Object System.Collections.Generic.List[string]

foreach ($name in $requiredInRoot) {
    $path = Join-Path $scriptDir $name
    if (-not (Test-Path $path)) {
        $missing.Add($name)
        continue
    }
    $item = Get-Item $path
    if ($item.Length -eq 0) {
        $empty.Add($name)
    }
}

if (-not (Test-Path $resultsDir)) {
    $missing.Add("results/")
} else {
    foreach ($name in $requiredInResults) {
        $path = Join-Path $resultsDir $name
        if (-not (Test-Path $path)) {
            $missing.Add("results/$name")
            continue
        }
        $item = Get-Item $path
        if ($item.Length -eq 0) {
            $empty.Add("results/$name")
        }
    }
}

Write-Host ""
Write-Host "Stage 1 output verification" -ForegroundColor Cyan
Write-Host "Script directory: $scriptDir"
Write-Host "Results directory: $resultsDir"
Write-Host "Required root files: $($requiredInRoot.Count)"
Write-Host "Required result files: $($requiredInResults.Count)"

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing files ($($missing.Count)):" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
}
if ($empty.Count -gt 0) {
    Write-Host ""
    Write-Host "Empty files ($($empty.Count)):" -ForegroundColor Yellow
    $empty | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
}

if ($missing.Count -eq 0 -and $empty.Count -eq 0) {
    Write-Host ""
    Write-Host "PASS: all required Stage 1 output files exist and are non-empty." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "FAIL: output verification failed. Regenerate artifacts and rerun." -ForegroundColor Red
exit 1

