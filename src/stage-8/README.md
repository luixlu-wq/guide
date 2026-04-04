# Stage 8 Runnable Runbook (Strict Execution)

This folder is the operatable execution guide for Stage 8 (fine-tuning methods).
Use it as a checklist and evidence workflow, not only as reference text.

---

## 1) Setup (Required)

Run inside `red-book/src/stage-8`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional richer path (CUDA and ecosystem packages):

```powershell
pip install -r requirements-optional.txt
```

---

## 2) Preflight Checks

```powershell
python --version
python -c "import numpy, sklearn; print('numpy/sklearn ready')"
python -c "import torch; print('torch', torch.__version__, 'cuda_available', torch.cuda.is_available())"
```

If torch is not installed, PyTorch/CUDA scripts still run with CPU fallback.

---

## 3) Run Modes

Fail-fast core path:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage8.ps1
```

Full ladder path (`simple -> intermediate -> advanced`):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage8.ps1
```

Ladder + labs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage8.ps1 -IncludeLabs
```

Ladder + labs + optional Qdrant compare lab:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage8.ps1 -IncludeLabs -IncludeQdrant
```

Notebook teaching path:

- `stage8_explainer.ipynb`

---

## 4) Data and Results

Data is generated deterministically by scripts using fixed seed.

All outputs are written to:

- `red-book/src/stage-8/results/`

Required run metadata in logs/reports:

- `dataset_version`
- `method/config version`
- `eval set policy`
- `promotion decision`

---

## 5) Script Matrix

Topics:

- `topic00a_pytorch_cuda_tuning_simple.py`
- `topic00_pytorch_cuda_tuning_intermediate.py`
- `topic00c_pytorch_cuda_tuning_advanced.py`
- `topic01a_dataset_schema_simple.py`
- `topic01_dataset_quality_intermediate.py`
- `topic01c_data_governance_advanced.py`
- `topic02a_sft_baseline_simple.py`
- `topic02_sft_intermediate.py`
- `topic02c_sft_eval_advanced.py`
- `topic03a_lora_simple.py`
- `topic03_lora_intermediate.py`
- `topic03c_lora_rank_sweep_advanced.py`
- `topic04a_qlora_simple.py`
- `topic04_qlora_intermediate.py`
- `topic04c_qlora_memory_tradeoff_advanced.py`
- `topic05a_distill_simple.py`
- `topic05_distill_intermediate.py`
- `topic05c_distill_eval_advanced.py`
- `topic06a_prompt_vs_tune_simple.py`
- `topic06_tune_vs_rag_intermediate.py`
- `topic06c_hybrid_strategy_advanced.py`
- `topic07a_eval_basics_simple.py`
- `topic07_eval_regression_intermediate.py`
- `topic07c_promotion_gate_advanced.py`
- `topic08a_model_registry_simple.py`
- `topic08_ops_observability_intermediate.py`
- `topic08c_canary_rollback_advanced.py`
- `topic09a_dpo_foundations_simple.py`
- `topic09_dpo_intermediate.py`
- `topic09c_dpo_eval_advanced.py`
- `topic10a_adapter_merge_simple.py`
- `topic10_adapter_merge_intermediate.py`
- `topic10c_task_arithmetic_advanced.py`
- `topic11a_synthetic_data_simple.py`
- `topic11_synthetic_data_curation_intermediate.py`
- `topic11c_synthetic_data_governance_advanced.py`
- `topic12a_memory_basics_simple.py`
- `topic12_memory_optimization_intermediate.py`
- `topic12c_flashattn_checkpointing_advanced.py`

Labs:

- `lab01_instruction_tuning_baseline.py`
- `lab02_lora_qlora_comparison.py`
- `lab03_distillation_tradeoff_lab.py`
- `lab04_finetune_project_baseline_to_production.py`
- `lab05_finetune_vs_rag_vs_hybrid_qdrant.py` (optional)

---

## 6) Required Lab Deliverables

Lab 1:

- `results/lab1_base_outputs.jsonl`
- `results/lab1_tuned_outputs.jsonl`
- `results/lab1_metrics_comparison.csv`
- `results/lab1_error_cases.md`

Lab 2:

- `results/lab2_lora_metrics.csv`
- `results/lab2_qlora_metrics.csv`
- `results/lab2_memory_latency_report.md`
- `results/stage8/vram_telemetry_5090.csv`
- `results/stage8/sft_vs_qlora_delta.md`

Lab 3:

- `results/lab3_teacher_outputs.jsonl`
- `results/lab3_student_outputs.jsonl`
- `results/lab3_distillation_report.md`
- `results/stage8/forgetting_test_results.jsonl`

Lab 4:

- `results/lab4_project_baseline_outputs.jsonl`
- `results/lab4_project_improved_outputs.jsonl`
- `results/lab4_solution_options.csv`
- `results/lab4_metrics_comparison.csv`
- `results/lab4_verification_report.md`
- `results/lab4_production_readiness.md`
- `results/stage8/model_promotion_report.md`

Lab 5 (optional Qdrant):

- `results/lab5_compare_prompt_rag_tune.csv`
- `results/lab5_qdrant_retrieval_metrics.csv`
- `results/lab5_final_decision.md`

---

## 7) One-Command Output Verification

Baseline labs (1-4):

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage8_outputs.ps1
```

Include optional Qdrant lab outputs:

```powershell
powershell -ExecutionPolicy Bypass -File .\verify_stage8_outputs.ps1 -IncludeQdrant
```

---

## 8) Troubleshooting Quick Guide

If scripts fail on imports:

1. verify venv is active
2. rerun `pip install -r requirements.txt`
3. check python path with `Get-Command python`

If CUDA path fails:

1. run CPU fallback path first
2. verify with `python -c "import torch; print(torch.cuda.is_available())"`

If Qdrant compare lab fails:

1. check `http://localhost:6333/collections`
2. rerun lab without `-IncludeQdrant`
3. inspect `results/lab5_qdrant_retrieval_metrics.csv`

---

## 9) Comment Standard (Mandatory)

All scripts include detailed comments for:

- data/schema declaration
- workflow steps
- expected outputs and interpretation
- error handling and fallback behavior
- before/after comparison logic
