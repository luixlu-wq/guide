"""Stage 6 Lab 03: Multi-agent ops assistant.

Deliverables:
- results/lab3_trace.json
- results/lab3_policy_decisions.csv
- results/lab3_incident_postmortem.md
"""

from __future__ import annotations

import json
from pathlib import Path

from stage6_utils import RESULTS_DIR, as_csv, print_data_declaration, summarize_incident


print_data_declaration("Lab03 Multi-Agent Ops Assistant")

# Simulated multi-agent workflow with coordinator and specialists.
trace = [
    {"step": 1, "agent": "coordinator", "action": "decompose_task", "status": "ok"},
    {"step": 2, "agent": "sre_agent", "action": "analyze_outage_signal", "status": "ok"},
    {"step": 3, "agent": "compliance_agent", "action": "policy_check_for_external_update", "status": "ok"},
    {"step": 4, "agent": "coordinator", "action": "request_human_approval", "status": "ok"},
    {"step": 5, "agent": "human_reviewer", "action": "approve_action", "status": "approved"},
]

trace_path = Path(RESULTS_DIR) / "lab3_trace.json"
trace_path.write_text(json.dumps(trace, indent=2), encoding="utf-8")

policy_rows = [
    {
        "decision_id": "PD-1",
        "check": "external_notification_requires_approval",
        "result": "pass_with_human_approval",
    },
    {
        "decision_id": "PD-2",
        "check": "sensitive_data_export_blocked",
        "result": "blocked",
    },
]
policy_path = Path(RESULTS_DIR) / "lab3_policy_decisions.csv"
as_csv(policy_path, policy_rows)

postmortem = summarize_incident(
    "LAB3-INC-01",
    "near_miss_external_update_without_initial_approval",
    "inserted_mandatory_hitl_gate_before_publish_step",
    "all future runs require explicit approval and pass policy checks",
)
postmortem_path = Path(RESULTS_DIR) / "lab3_incident_postmortem.md"
postmortem_path.write_text(postmortem, encoding="utf-8")

print("\nLab03 completed. Deliverables:")
print(f"- {trace_path}")
print(f"- {policy_path}")
print(f"- {postmortem_path}")
