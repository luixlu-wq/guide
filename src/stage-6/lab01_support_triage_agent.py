"""Stage 6 Lab 01: Support triage agent with safety and eval.

Deliverables written by this script:
- results/stage6_lab_outputs.jsonl
- results/stage6_lab_metrics.csv
- results/stage6_lab_trace.json
- results/stage6_lab_failure_log.md
- results/stage6_lab_before_after.md
"""

from __future__ import annotations

import json
from pathlib import Path

from stage6_utils import (
    RESULTS_DIR,
    as_jsonl,
    ensure_ticket_dataset,
    evaluate_predictions,
    load_eval_ids,
    load_ticket_rows,
    print_data_declaration,
    run_agent_loop,
    run_workflow_baseline,
    select_eval_tickets,
)


print_data_declaration("Lab01 Support Triage Agent")
ensure_ticket_dataset()

rows = load_ticket_rows()
eval_rows = select_eval_tickets(rows, load_eval_ids())

# Baseline workflow run.
baseline_outputs = [run_workflow_baseline(row) for row in eval_rows]
baseline_metrics = evaluate_predictions(baseline_outputs)

# Agent run after controlled improvement (full 4-step policy-aware loop).
agent_outputs = [run_agent_loop(row, max_steps=4) for row in eval_rows]
agent_metrics = evaluate_predictions(agent_outputs)

# Persist final outputs from improved run.
outputs_path = Path(RESULTS_DIR) / "stage6_lab_outputs.jsonl"
as_jsonl(outputs_path, agent_outputs)

# Save metrics comparison in one CSV.
metrics_rows = [
    {"label": "baseline_workflow", **baseline_metrics},
    {"label": "agent_improved", **agent_metrics},
]

from stage6_utils import as_csv  # local import keeps top section focused for students.

metrics_path = Path(RESULTS_DIR) / "stage6_lab_metrics.csv"
as_csv(metrics_path, metrics_rows)

# Build trace artifact from agent run.
trace = []
for out in agent_outputs:
    trace.append(
        {
            "ticket_id": out["ticket_id"],
            "tool_calls": out.get("tool_calls", []),
            "trace_steps": out.get("trace_steps", []),
            "failure_class": out.get("failure_class"),
        }
    )
trace_path = Path(RESULTS_DIR) / "stage6_lab_trace.json"
trace_path.write_text(json.dumps(trace, indent=2), encoding="utf-8")

# Failure log artifact.
failures = [out for out in agent_outputs if out.get("failure_class")]
failure_log_path = Path(RESULTS_DIR) / "stage6_lab_failure_log.md"
failure_log_path.write_text(
    "\n".join(
        [
            "# Stage 6 Failure Log",
            f"total_cases={len(agent_outputs)}",
            f"failure_cases={len(failures)}",
            "",
            "## Failure Details",
        ]
        + [f"- ticket={row['ticket_id']} | failure={row['failure_class']}" for row in failures]
    ),
    encoding="utf-8",
)

# Before/after report artifact.
before_after_path = Path(RESULTS_DIR) / "stage6_lab_before_after.md"
before_after_path.write_text(
    "\n".join(
        [
            "# Stage 6 Before/After Summary",
            "",
            "## Baseline metrics",
            str(baseline_metrics),
            "",
            "## Agent improved metrics",
            str(agent_metrics),
            "",
            "## Controlled improvement",
            "Used max_steps=4 and explicit policy_gate step to reduce premature-stop failures.",
        ]
    ),
    encoding="utf-8",
)

print("\nLab01 completed. Deliverables:")
print(f"- {outputs_path}")
print(f"- {metrics_path}")
print(f"- {trace_path}")
print(f"- {failure_log_path}")
print(f"- {before_after_path}")
