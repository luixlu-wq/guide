# Stage 14 - Hedge-Fund Style AI Trading System

**Week 24-25**

---

## 0) If This Chapter Feels Hard

Use this sequence:

1. learn portfolio and risk fundamentals first
2. build multi-asset baseline with fixed assumptions
3. add risk engine and allocation constraints
4. model execution costs and stress scenarios
5. verify strategy updates with controlled reruns

This chapter moves from signal quality to portfolio survivability.

---

## 1) Stage Goal

Upgrade single-model thinking into portfolio-level trading system engineering.

You must be able to:

- manage multi-asset data and features
- build signal-to-position workflow with risk controls
- optimize allocations under constraints
- simulate realistic execution costs and slippage
- evaluate with return + risk metrics
- troubleshoot under stress and recovery scenarios

---

## 2) System Mental Model

Reference flow:

`multi-asset data -> features -> alpha signals -> risk engine -> portfolio optimizer -> execution simulation -> performance and stress evaluation`

### Core principle

Prediction quality is necessary but not sufficient. Risk and execution can dominate final results.

### Non-negotiable controls

- position limits
- exposure limits
- drawdown guards
- turnover constraints
- transaction-cost modeling

---

## 3) Multi-Asset Data and Feature Foundations

### What it is

Unified ingestion and normalization for multiple assets.

### Why it matters

Portfolio logic fails when assets are misaligned or inconsistently processed.

### Operatable checklist

1. align symbols by date index
2. validate coverage and missingness
3. standardize schema per symbol
4. version data snapshot

### Typical issues

- misaligned dates
- missing bars by symbol
- unstable derived features due to sparse data

### Related scripts

- `topic00*_trading_system_basics_*`
- `topic01*_signal_quality_*`

---

## 4) Module A - Signal Quality Management

### What it is

Converts features into candidate alpha signals.

### Why it matters

Weak or unstable signals create high turnover and poor risk-adjusted return.

### Operatable checklist

1. evaluate signal precision/recall or error profile
2. segment by asset and regime
3. filter unstable signals
4. freeze signal version per run

### Typical issues

- signal decay after regime shift
- high false positives
- instability across assets

### Metrics

- hit rate
- information coefficient (if available)
- stability by regime

### Related scripts

- `topic01*_signal_quality_*`

---

## 5) Module B - Risk Engine

### What it is

Translates raw signals into risk-budgeted candidate positions.

### Why it matters

Without risk engine, one strong signal can create portfolio fragility.

### Required controls

- max position size
- sector/asset exposure caps
- volatility scaling
- drawdown triggers
- stop-loss policy (if applicable)

### Typical issues

- concentrated exposure
- hidden correlation clusters
- drawdown escalation during stress

### Related scripts

- `topic02*_risk_engine_*`
- `lab02_risk_engine_improvement.py`

---

## 6) Module C - Portfolio Optimization

### What it is

Selects final portfolio weights under constraints.

### Why it matters

Allocation determines realized risk-return profile.

### Operatable checklist

1. define objective function
2. define hard constraints
3. solve for weights
4. validate turnover and concentration

### Common objective examples

- maximize expected return under risk target
- maximize Sharpe proxy under constraints
- minimize variance under expected return floor

### Typical issues

- optimizer instability
- corner solutions (all weight in one asset)
- high turnover from noisy expected returns

### Related scripts

- `topic03*_portfolio_optimizer_*`

---

## 7) Module D - Execution Simulation

### What it is

Converts target weights into realistic executed trades.

### Why it matters

Ignoring costs and slippage overstates strategy quality.

### Required execution assumptions

- transaction fee model
- slippage model
- liquidity cap
- fill delay assumption

### Typical issues

- unrealistic fills
- cost blow-up at turnover spikes
- execution delay reducing edge

### Related scripts

- `topic04*_execution_sim_*`
- `lab03_execution_slippage_impact.py`

---

## 8) Module E - Stress Testing and Tail Risk

### What it is

Evaluates strategy behavior under adverse scenarios.

### Why it matters

Production-grade systems must survive unfavorable conditions, not only average periods.

### Required stress tests

- volatility spike scenario
- correlation spike scenario
- liquidity shock scenario
- data outage or delayed feed scenario

### Typical issues

- drawdown exceeds tolerance
- diversification breaks under stress
- recovery time too long

### Related scripts

- `topic05*_stress_test_*`
- `lab04_stress_test_and_recovery.py`

---

## 9) Module F - Operations and Governance

### What it is

Controls for strategy change management and auditability.

### Required governance artifacts

- strategy change log
- risk-limit checklist
- release gate report
- rollback trigger definition

### Typical issues

- undocumented strategy changes
- no clear approval path
- weak post-incident learning

### Related scripts

- `topic06*_ops_governance_*`

---

## 10) PyTorch and CUDA in Portfolio Systems

### Why this is required

Signal generation and scenario simulation can become compute-intensive; runtime profiling affects deployment design.

### Required checks

1. compare CPU vs CUDA inference path for signal generation
2. monitor memory usage under multi-asset batch runs
3. define fallback path if CUDA unavailable
4. include runtime evidence in release package

---

## 11) Data Declaration Standard

Every example must include:

```text
Data: <name and source>
Records/Samples: <count>
Input schema: <fields and types>
Output schema: <fields and types>
Eval policy: <fixed backtest window and assumptions>
Type: <signal/risk/optimizer/execution/stress/ops>
```

---

## 12) Example Complexity Scale

- L1 Simple: single-strategy baseline with fixed assumptions
- L2 Intermediate: compare two risk or allocation variants
- L3 Advanced: stress scenario plus release/rollback decision

Where complexity is:

- multi-asset data alignment
- correlation and exposure interactions
- execution realism
- stress evaluation and governance decisions

---

## 13) Stage 14 Script Mapping

Target package: `red-book/src/stage-14/`

Topics:

- `topic00*_trading_system_basics_*`
- `topic01*_signal_quality_*`
- `topic02*_risk_engine_*`
- `topic03*_portfolio_optimizer_*`
- `topic04*_execution_sim_*`
- `topic05*_stress_test_*`
- `topic06*_ops_governance_*`

Labs:

- `lab01_multi_asset_baseline.py`
- `lab02_risk_engine_improvement.py`
- `lab03_execution_slippage_impact.py`
- `lab04_stress_test_and_recovery.py`

Script requirements:

- detailed functional comments
- deterministic reruns
- explicit failure paths
- metric artifacts under `results/`

---

## 14) Practice Labs (Detailed)

## Lab 1: Multi-Asset Baseline

Goal:

- produce initial multi-asset strategy baseline.

Required outputs:

- `results/lab1_multi_asset_baseline_metrics.csv`
- `results/lab1_signal_summary.csv`
- `results/lab1_portfolio_weights.csv`

## Lab 2: Risk Engine Improvement

Goal:

- reduce drawdown while preserving acceptable return.

Required outputs:

- `results/lab2_risk_before_after.csv`
- `results/lab2_constraint_changes.csv`
- `results/lab2_risk_decision.md`

## Lab 3: Execution Slippage Impact

Goal:

- quantify impact of execution assumptions.

Required outputs:

- `results/lab3_execution_cost_profile.csv`
- `results/lab3_slippage_scenarios.csv`
- `results/lab3_execution_findings.md`

## Lab 4: Stress Test and Recovery

Goal:

- test survival and recovery under adverse scenarios.

Required outputs:

- `results/lab4_stress_results.csv`
- `results/lab4_recovery_actions.csv`
- `results/lab4_release_recommendation.md`

---

## 15) Troubleshooting Standard (Identify -> Compare -> Verify)

1. reproduce failure with fixed scenario set
2. classify domain (`signal`, `risk`, `optimizer`, `execution`, `stress`, `ops`)
3. compare two remediation options
4. apply one controlled change
5. rerun identical scenarios
6. verify deltas and update decision

---

## 16) Industry Pain-Point Matrix

| Topic | Pain point | Root causes | Resolution | Related lab |
|---|---|---|---|---|
| Signal quality | alpha decays quickly | regime shift, unstable features | regime-aware evaluation and filtering | `lab01_multi_asset_baseline.py` |
| Risk engine | large unexpected drawdowns | weak exposure constraints | stricter limits and drawdown controls | `lab02_risk_engine_improvement.py` |
| Optimizer | unstable allocations | noisy expectations, weak constraints | robust constraints and turnover controls | `topic03*_portfolio_optimizer_*` |
| Execution | paper alpha disappears live | ignored slippage and costs | realistic execution simulation | `lab03_execution_slippage_impact.py` |
| Stress resilience | strategy fails in shocks | no stress assumptions | stress testing and recovery workflow | `lab04_stress_test_and_recovery.py` |

---

## 17) Self-Test (Readiness)

1. Can you explain why prediction quality alone is insufficient?
2. Can you enforce exposure and drawdown controls?
3. Can you justify allocation constraints?
4. Can you model execution costs realistically?
5. Can you run and interpret stress tests?
6. Can you make release or rollback decisions with evidence?

If fewer than 5/6 are operationally answerable, rerun labs 2-4.

---

## 18) Resource Library

- PyPortfolioOpt docs: https://pyportfolioopt.readthedocs.io/
- cvxpy docs: https://www.cvxpy.org/
- Backtrader docs: https://www.backtrader.com/docu/
- Pandas docs: https://pandas.pydata.org/docs/
- scikit-learn docs: https://scikit-learn.org/stable/

---

## 19) What Comes After Stage 14

Stage 15 focuses on systematic diagnosis and improvement when models or systems underperform.

## 20) Missing-Item Gap Closure (Stage 14 Addendum)

This section closes remaining gaps and makes Stage 14 trading operations more realistic and executable.

Mandatory additions for this chapter:
- deeper linkage between signal quality, risk controls, and execution costs
- explicit failure signatures for each module
- command-level lab operations with net-of-cost evaluation
- strict stress-test and governance gate criteria

## 21) Stage 14 Topic-by-Topic Deepening Matrix

| Module | Theory Deepening | Operatable Tutorial Requirement | Typical Failure Signature | Required Evidence | Script/Lab |
|---|---|---|---|---|---|
| Data Foundations | Data integrity, leakage, survivorship bias, timestamp integrity | Run data audit and leak-safe split checks before model runs | Backtest looks strong but fails in realistic replay | `results/stage14/data_audit.md` | `topic00_trading_system_basics` + `lab01_multi_asset_baseline.py` |
| Signal Quality | IC/IR stability and regime sensitivity theory | Evaluate rolling-window stability and decay signals | Signal decays quickly after small regime shift | `results/stage14/signal_stability_report.csv` | `topic01_signal_quality` + `lab01_multi_asset_baseline.py` |
| Risk Engine | VaR/ES/max drawdown controls and kill-switch policy | Implement hard limits and breach handling runbook | Drawdown breaches policy in high-volatility window | `results/stage14/risk_control_matrix.csv` | `topic02_risk_engine` + `lab02_risk_engine_improvement.py` |
| Portfolio Optimization | Constraint/regularization/turnover tradeoff | Run constrained optimizer and compare turnover-aware metrics | Unstable weights and excessive turnover | `results/stage14/optimizer_constraint_report.md` | `topic03_portfolio_optimizer` + `lab02_risk_engine_improvement.py` |
| Execution Simulation | Slippage/spread/impact decomposition theory | Simulate execution costs and compare gross vs net performance | Gross alpha disappears net of costs | `results/stage14/slippage_decomposition.csv` | `topic04_execution_sim` + `lab03_execution_slippage_impact.py` |
| Stress Testing | Tail-risk scenario theory and recovery design | Run stress pack and define recovery sequence | Strategy fails under shock scenarios with no response path | `results/stage14/stress_pack.md` + `recovery_runbook.md` | `topic05_stress_test` + `lab04_stress_test_and_recovery.py` |

## 22) Stage 14 Lab Operation Runbook (Command-Level)

### Lab 1: Multi-Asset Baseline
- Command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab01_multi_asset_baseline`
- Required outputs:
  - `results/stage14/baseline_signal_report.csv`
  - `results/stage14/data_audit.md`
- Pass criteria:
  - Baseline is leak-safe with stable initial signal diagnostics.
- First troubleshooting action:
  - Verify symbol mapping and rolling split integrity.

### Lab 2: Risk Engine Improvement
- Command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab02_risk_engine_improvement`
- Required outputs:
  - `results/stage14/risk_before_after.csv`
  - `results/stage14/risk_policy_note.md`
- Pass criteria:
  - Risk breaches decrease while target performance remains acceptable.
- First troubleshooting action:
  - Compare two risk-limit configurations before deciding final policy.

### Lab 3: Execution Slippage Impact
- Command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab03_execution_slippage_impact`
- Required outputs:
  - `results/stage14/slippage_decomposition.csv`
  - `results/stage14/execution_recommendation.md`
- Pass criteria:
  - Net-of-cost metrics remain above minimum acceptance threshold.
- First troubleshooting action:
  - Reduce turnover and rerun under fixed assumptions if net metrics fail.

### Lab 4: Stress Test and Recovery
- Command: `pwsh red-book/src/stage-14/run_all_stage14.ps1 -Lab lab04_stress_test_and_recovery`
- Required outputs:
  - `results/stage14/stress_pack.md`
  - `results/stage14/recovery_runbook.md`
- Pass criteria:
  - Tail-risk behavior documented with operational recovery path.
- First troubleshooting action:
  - Define kill-switch trigger and staged re-enable criteria.

## 23) Stage 14 Resource-to-Module Mapping (Must Cite in Chapter Text)

- Portfolio optimization: PyPortfolioOpt docs
- Backtesting/execution workflow: Backtrader docs
- Financial ML and robustness: Advances in Financial Machine Learning
- Statistical diagnostics: statsmodels docs
- Data/ML implementation: pandas and scikit-learn docs
- Runtime evidence path: PyTorch CUDA notes

Requirement: each module tutorial must cite at least one mapped source.

## 24) Stage 14 Production Review Rubric (Hard Gates)

- leakage checks pass before any strategy performance claim
- risk policy thresholds pass in baseline and stress scenarios
- all decisions use net-of-cost metrics (not gross-only)
- strategy changes are auditable and rollback-ready
- all improvement claims include before/after artifacts

If any hard gate fails: decision cannot be `promote`.
