param(
    [string]$PythonExe = "python",
    [switch]$IncludeGpu
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:LOKY_MAX_CPU_COUNT = "1"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic01_linear_regression.py",
    "topic02_logistic_regression.py",
    "topic03_decision_tree_depth.py",
    "topic04_random_forest_baseline.py",
    "topic05_svm_tuning.py",
    "topic06_kmeans_silhouette.py",
    "topic07_fair_model_comparison.py",
    "topic08_failure_modes_overfit_leakage.py"
)

if ($IncludeGpu) {
    $scripts += "topic09_pytorch_cuda_bridge.py"
}

$requiredArtifacts = @{
    "topic05_svm_tuning.py" = @(
        "results/stage3/topic05_svm_summary.csv",
        "results/stage3/topic05_svm_summary.json"
    )
    "topic06_kmeans_silhouette.py" = @(
        "results/stage3/topic06_kmeans_k_scan.csv",
        "results/stage3/topic06_kmeans_k_scan.json"
    )
    "topic07_fair_model_comparison.py" = @(
        "results/topic07_fair_comparison.csv",
        "results/stage3/model_compare_before_after.csv",
        "results/stage3/model_compare_seed_stability.csv"
    )
    "topic08_failure_modes_overfit_leakage.py" = @(
        "results/stage3/failure_class_before_after.csv",
        "results/stage3/failure_diagnosis.md"
    )
    "topic09_pytorch_cuda_bridge.py" = @(
        "results/stage3/cpu_gpu_latency_transfer.csv",
        "results/stage3/decision_and_risk.md"
    )
}

Write-Host "Stage 3 fail-fast runner" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
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

    if ($requiredArtifacts.ContainsKey($name)) {
        foreach ($artifactRel in $requiredArtifacts[$name]) {
            $artifactPath = Join-Path $scriptDir $artifactRel
            if (-not (Test-Path $artifactPath)) {
                throw "Artifact missing after ${name}: $artifactPath"
            }
        }
    }
}

# Sanity checks for key benchmark artifacts.
$topic07Path = Join-Path $scriptDir "results/stage3/model_compare_before_after.csv"
if (Test-Path $topic07Path) {
    $topic07 = Import-Csv -Path $topic07Path
    if ($topic07.Count -lt 4) {
        throw "Sanity check failed: topic07 comparison has fewer than 4 models."
    }
    foreach ($row in $topic07) {
        $f1 = [double]$row.test_f1
        if ($f1 -lt 0.5) {
            throw "Sanity check failed: test_f1 below 0.5 in topic07 artifact."
        }
    }
}

Write-Host ""
Write-Host "All Stage 3 scripts completed successfully." -ForegroundColor Green
