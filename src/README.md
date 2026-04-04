# Red-Book Stage Runner (Stage 10-16)

This folder provides a single entry point to run or verify the advanced stages.

## Coverage

- Stage 10: Final AI System
- Stage 11: AI Infrastructure
- Stage 12: AI System Architecture Patterns
- Stage 13: Capstone Delivery Project
- Stage 14: Hedge-Fund Style AI Trading System
- Stage 15: Systematic Troubleshooting
- Stage 16: Mastery and Industry Readiness

## One-Command Orchestrator

Use `run_all_stage10_16.ps1` from `red-book/src`.

### 1) Fail-fast run for all stages

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage10_16.ps1 -Mode fail-fast
```

### 2) Ladder run for all stages (topic simple -> intermediate -> advanced)

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage10_16.ps1 -Mode ladder
```

### 3) Ladder + labs for all stages

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage10_16.ps1 -Mode ladder -IncludeLabs
```

### 4) Verify required lab artifacts for all stages

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage10_16.ps1 -Mode verify
```

## Optional Parameters

- `-Stages` to run a subset, example:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage10_16.ps1 -Mode verify -Stages 13,14,15
```

- `-PythonExe` to set Python executable:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_stage10_16.ps1 -Mode fail-fast -PythonExe python
```

## Per-Stage Details

Each stage has its own runbook:

- `red-book/src/stage-10/README.md`
- `red-book/src/stage-11/README.md`
- `red-book/src/stage-12/README.md`
- `red-book/src/stage-13/README.md`
- `red-book/src/stage-14/README.md`
- `red-book/src/stage-15/README.md`
- `red-book/src/stage-16/README.md`
