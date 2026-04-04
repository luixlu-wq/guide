# Stage 5 Runnable Examples

This folder contains complete runnable examples for Stage 5: tokenization, prompt engineering, structured output, RAG, and reliability evaluation.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional packages for expanded experiments:

```powershell
pip install -r requirements-optional.txt
```

## Run

Fail-fast core path:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage5.ps1
```

Ladder path (simple -> intermediate -> advanced):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage5.ps1
```

Include the multi-head attention bridge before ladders:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage5.ps1 -IncludeBridge
```

Include review deep-dive modules (Transformer mechanics + tokenizer comparison + CoT):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage5.ps1 -IncludeDeepDive
```

Include the step-by-step multi-head-attention mini-LLM lab:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_ladder_stage5.ps1 -IncludeBridge -IncludeLab
python .\lab01_simple_mha_llm.py
```

## Topics

- PyTorch/CUDA ladder:
  - `topic00a_pytorch_cuda_simple.py`
  - `topic00_pytorch_cuda_intermediate.py`
  - `topic00c_pytorch_cuda_advanced.py`
- Multi-head attention bridge:
  - `topic01_multihead_attention.py`
- Review deep-dive modules:
  - `topic05a_attention_math.py`
  - `topic05b_min_transformer.py`
  - `topic05c_vram_optimization.py`
  - `topic06a_tokenizer_comparison.py`
  - `topic07c_chain_of_thought.py`
- Tokenization ladder:
  - `topic01a_tokenization_simple.py`
  - `topic01_tokenization_intermediate.py`
  - `topic01c_tokenization_advanced.py`
- Prompting ladder:
  - `topic02a_prompting_simple.py`
  - `topic02_prompting_intermediate.py`
  - `topic02c_prompting_advanced.py`
- Structured output ladder:
  - `topic03a_structured_output_simple.py`
  - `topic03_structured_output_intermediate.py`
  - `topic03c_structured_output_advanced.py`
- RAG ladder:
  - `topic04a_rag_simple.py`
  - `topic04_rag_intermediate.py`
  - `topic04c_rag_advanced.py`
- Embeddings ladder:
  - `topic05a_embeddings_simple.py`
  - `topic05_embeddings_intermediate.py`
  - `topic05c_embeddings_advanced.py`
- Multi-head-attention mini-LLM lab:
  - `lab01_simple_mha_llm.py`
- Reliability + project:
  - `topic07_prompt_eval_regression.py`
  - `topic08_project_baseline.py`

## Outputs

`topic08_project_baseline.py` creates:

- `results/raw_outputs_before.jsonl`
- `results/raw_outputs_after.jsonl`
- `results/metrics_before.csv`
- `results/metrics_after.csv`
- `results/format_validity_report.json`
- `results/hallucination_audit.md`
- `results/final_prompt_selection.md`
- `results/reproducibility.md`

## Data Source and Structure Summary

- Tokenization/Prompting/Structured examples:
  - In-script educational text samples with fixed schemas
- RAG examples:
  - In-script document corpora with fields `{id,title,content}`
  - Query sets with optional gold supporting document IDs
- Embedding examples:
  - In-script sentence corpora
  - Dense vector outputs and retrieval metrics (`hit@k`, ranking scores)
- PyTorch/CUDA examples:
  - Device selection and tensor operations
  - Device-aware training loops (CPU/GPU)
  - Optional mixed precision on CUDA
- Multi-head-attention mini-LLM lab:
  - In-script tiny corpus for next-token prediction
  - Character-ID windows with fixed train/validation split
- Reliability/project examples:
  - In-script fixed datasets for reproducible prompt version comparisons
