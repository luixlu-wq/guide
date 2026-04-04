param(
    [string]$PythonExe = "python",
    [switch]$IncludeBridge,
    [switch]$IncludeLab
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_pytorch_cuda_simple.py",
    "topic00_pytorch_cuda_intermediate.py",
    "topic00c_pytorch_cuda_advanced.py",
    "topic01a_tokenization_simple.py",
    "topic01_tokenization_intermediate.py",
    "topic01c_tokenization_advanced.py",
    "topic02a_prompting_simple.py",
    "topic02_prompting_intermediate.py",
    "topic02c_prompting_advanced.py",
    "topic03a_structured_output_simple.py",
    "topic03_structured_output_intermediate.py",
    "topic03c_structured_output_advanced.py",
    "topic04a_rag_simple.py",
    "topic04_rag_intermediate.py",
    "topic04c_rag_advanced.py",
    "topic05a_embeddings_simple.py",
    "topic05_embeddings_intermediate.py",
    "topic05c_embeddings_advanced.py"
)

if ($IncludeBridge) {
    $scripts = @("topic01_multihead_attention.py") + $scripts
}

if ($IncludeLab) {
    $scripts = $scripts + @("lab01_simple_mha_llm.py")
}

Write-Host "Stage 5 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include multi-head bridge: $IncludeBridge"
Write-Host "Include simple MHA LLM lab: $IncludeLab"

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
Write-Host "All Stage 5 ladder scripts completed successfully." -ForegroundColor Green
