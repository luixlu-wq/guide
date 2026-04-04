# Stage 7 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 7 (RAG systems).
Use it as a checklist, not only as reference text.

---

## 1) Setup (Required)

Run inside `red-book/src/stage-7`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional for richer experiments (CUDA + vector DB extras):

```powershell
pip install -r requirements-optional.txt
```

---

## 2) Preflight Checks (Run Before Any Lab)

```powershell
python --version
python -c "import torch; print('torch', torch.__version__, 'cuda_available', torch.cuda.is_available())"
python -c "import platform; print(platform.platform())"
```

If you use local Qdrant:

1. Confirm service on `localhost:6333`.
2. Open `http://localhost:6333/collections`.
3. If unavailable, skip Qdrant scripts and run CPU/offline path first.

---

## 3) Run Modes

Fail-fast core path:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage7.ps1
```

Full ladder path (`simple -> intermediate -> advanced`):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage7.ps1
```

Ladder + labs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage7.ps1 -IncludeLabs
```

Ladder + Qdrant:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage7.ps1 -IncludeQdrant
```

Ladder + labs + Qdrant:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage7.ps1 -IncludeLabs -IncludeQdrant
```

Notebook teaching path:

- `stage7_explainer.ipynb`

---

## 4) Data, Output Folder, and Version Logging

Input data is auto-generated on first run:

- `red-book/data/stage-7/docs_stage7.jsonl`
- `red-book/data/stage-7/eval_queries_stage7.jsonl`

All outputs are written to:

- `red-book/src/stage-7/results/`

For every lab run, log these version tags in terminal and report files:

- `dataset_version`
- `eval_set_version`
- `retrieval_config_version`
- `prompt_version`

---

## 5) Lab Execution Matrix (Required Outputs)

Lab 1:

- script: `lab01_pdf_qa_rag.py`
- outputs:
  - `results/lab1_outputs.jsonl`
  - `results/lab1_retrieval_metrics.csv`
  - `results/lab1_grounding_audit.md`

Lab 2:

- script: `lab02_policy_assistant_rag.py`
- outputs:
  - `results/lab2_outputs.jsonl`
  - `results/lab2_policy_violations.csv`
  - `results/lab2_fix_log.md`

Lab 3:

- script: `lab03_hybrid_retrieval_benchmark.py`
- outputs:
  - `results/lab3_retrieval_comparison.csv`
  - `results/lab3_error_cases.md`
  - `results/lab3_before_after_summary.md`

Lab 4:

- script: `lab04_enterprise_rag_operations.py`
- outputs:
  - `results/lab4_sync_log.md`
  - `results/lab4_acl_validation.csv`
  - `results/lab4_slo_report.csv`
  - `results/lab4_incident_postmortem.md`

Lab 5 (Qdrant):

- script: `lab05_qdrant_end_to_end_rag.py`
- outputs:
  - `results/lab5_qdrant_outputs.jsonl`
  - `results/lab5_qdrant_metrics.csv`
  - `results/lab5_qdrant_acl_validation.csv`
  - `results/lab5_qdrant_runbook.md`

Lab 6 (Baseline -> Production):

- script: `lab06_project_baseline_to_production.py`
- outputs:
  - `results/lab6_project_baseline_outputs.jsonl`
  - `results/lab6_project_improved_outputs.jsonl`
  - `results/lab6_project_solution_options.csv`
  - `results/lab6_project_metrics_comparison.csv`
  - `results/lab6_project_verification_report.md`
  - `results/lab6_project_production_readiness.md`

---

## 6) Strict Lab Workflow (Use For Every Lab)

1. Run baseline with fixed dataset and fixed eval ids.
2. Save baseline outputs.
3. Apply one controlled change only.
4. Rerun with same eval ids.
5. Compare before/after metrics (`hit@k`, `MRR`, groundedness, citation precision, latency, cost).
6. Record decision (`promote`, `hold`, `rollback`) with reason.

Do not change multiple variables in the same experiment.

---

## 7) Fast Validation Commands

Check all expected outputs exist:

```powershell
$required = @(
  'lab1_outputs.jsonl','lab1_retrieval_metrics.csv','lab1_grounding_audit.md',
  'lab2_outputs.jsonl','lab2_policy_violations.csv','lab2_fix_log.md',
  'lab3_retrieval_comparison.csv','lab3_error_cases.md','lab3_before_after_summary.md',
  'lab4_sync_log.md','lab4_acl_validation.csv','lab4_slo_report.csv','lab4_incident_postmortem.md',
  'lab6_project_baseline_outputs.jsonl','lab6_project_improved_outputs.jsonl',
  'lab6_project_solution_options.csv','lab6_project_metrics_comparison.csv',
  'lab6_project_verification_report.md','lab6_project_production_readiness.md'
)
$missing = $required | Where-Object { -not (Test-Path (Join-Path .\results $_)) }
if ($missing.Count -eq 0) { 'All required baseline outputs exist.' } else { 'Missing:'; $missing }
```

Check Qdrant-specific output files:

```powershell
$qdrantRequired = @(
  'lab5_qdrant_outputs.jsonl','lab5_qdrant_metrics.csv',
  'lab5_qdrant_acl_validation.csv','lab5_qdrant_runbook.md'
)
$missing = $qdrantRequired | Where-Object { -not (Test-Path (Join-Path .\results $_)) }
if ($missing.Count -eq 0) { 'All Qdrant outputs exist.' } else { 'Missing:'; $missing }
```

One-command validator (recommended):

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage7_outputs.ps1
```

Include Qdrant deliverables:

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage7_outputs.ps1 -IncludeQdrant
```

---

## 8) Troubleshooting Quick Guide

If scripts fail immediately:

1. confirm venv is active
2. rerun `pip install -r requirements.txt`
3. verify Python path:
   - `Get-Command python`

If CUDA path fails:

1. run CPU fallback by default
2. check:
   - `python -c "import torch; print(torch.cuda.is_available())"`

If Qdrant path fails:

1. check `http://localhost:6333/collections`
2. run non-Qdrant scripts first
3. rerun:
   - `python .\topic02d_qdrant_local_index.py`
   - `python .\topic03d_qdrant_acl_search.py`

---

## 9) Topic Mapping

- PyTorch/CUDA:
  - `topic00a_pytorch_cuda_rag_simple.py`
  - `topic00_pytorch_cuda_rag_intermediate.py`
  - `topic00c_pytorch_cuda_rag_advanced.py`
- Ingestion/chunking:
  - `topic01a_ingestion_chunking_simple.py`
  - `topic01_ingestion_chunking_intermediate.py`
  - `topic01c_chunk_quality_advanced.py`
- Embeddings/index:
  - `topic02a_embeddings_index_simple.py`
  - `topic02_embeddings_index_intermediate.py`
  - `topic02c_index_diagnostics_advanced.py`
  - `topic02d_qdrant_local_index.py`
- Retrieval/rerank/hybrid:
  - `topic03a_retrieval_simple.py`
  - `topic03_retrieval_rerank_intermediate.py`
  - `topic03c_hybrid_retrieval_advanced.py`
  - `topic03d_qdrant_acl_search.py`
- Prompt/grounding:
  - `topic04a_prompt_context_simple.py`
  - `topic04_grounding_intermediate.py`
  - `topic04c_citation_guardrails_advanced.py`
- Evaluation/regression:
  - `topic05a_eval_basics_simple.py`
  - `topic05_eval_metrics_intermediate.py`
  - `topic05c_regression_suite_advanced.py`
- Operations:
  - `topic06a_index_freshness_simple.py`
  - `topic06_ops_cost_latency_intermediate.py`
  - `topic06c_acl_incident_advanced.py`
- Baseline local example:
  - `stage7_minimal_local_rag.py`

---

## 10) Script Comment Standard (Mandatory)

All scripts must include detailed comments for:

- data source and schema declaration
- function responsibilities
- workflow steps
- expected output interpretation
- failure handling and reliability checks
