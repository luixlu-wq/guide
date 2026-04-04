param(
    [string]$PythonExe = "python",
    [switch]$IncludeLabs,
    [switch]$IncludeQdrant
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = @(
    "topic00a_pytorch_cuda_rag_simple.py",
    "topic00_pytorch_cuda_rag_intermediate.py",
    "topic00c_pytorch_cuda_rag_advanced.py",
    "topic01a_ingestion_chunking_simple.py",
    "topic01_ingestion_chunking_intermediate.py",
    "topic01c_chunk_quality_advanced.py",
    "topic02a_embeddings_index_simple.py",
    "topic02_embeddings_index_intermediate.py",
    "topic02c_index_diagnostics_advanced.py",
    "topic03a_retrieval_simple.py",
    "topic03_retrieval_rerank_intermediate.py",
    "topic03c_hybrid_retrieval_advanced.py",
    "topic04a_prompt_context_simple.py",
    "topic04_grounding_intermediate.py",
    "topic04c_citation_guardrails_advanced.py",
    "topic05a_eval_basics_simple.py",
    "topic05_eval_metrics_intermediate.py",
    "topic05c_regression_suite_advanced.py",
    "topic06a_index_freshness_simple.py",
    "topic06_ops_cost_latency_intermediate.py",
    "topic06c_acl_incident_advanced.py"
)

if ($IncludeLabs) {
    $scripts = $scripts + @(
        "lab01_pdf_qa_rag.py",
        "lab02_policy_assistant_rag.py",
        "lab03_hybrid_retrieval_benchmark.py",
        "lab04_enterprise_rag_operations.py",
        "lab06_project_baseline_to_production.py"
    )
}

if ($IncludeQdrant) {
    $scripts = $scripts + @(
        "topic02d_qdrant_local_index.py",
        "topic03d_qdrant_acl_search.py"
    )

    if ($IncludeLabs) {
        $scripts = $scripts + @(
            "lab05_qdrant_end_to_end_rag.py"
        )
    }
}

Write-Host "Stage 7 ladder runner (simple -> intermediate -> advanced)" -ForegroundColor Cyan
Write-Host "Python executable: $PythonExe"
Write-Host "Script directory : $scriptDir"
Write-Host "Include labs: $IncludeLabs"
Write-Host "Include Qdrant: $IncludeQdrant"

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
Write-Host "All Stage 7 ladder scripts completed successfully." -ForegroundColor Green
