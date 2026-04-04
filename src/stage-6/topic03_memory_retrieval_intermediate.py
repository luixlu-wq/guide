"""Stage 6 Topic 03: Memory retrieval + checkpoint rehydration (intermediate).

What this script teaches:
1. Retrieve relevant memory records for an agent query.
2. Persist checkpoint state after each major step.
3. Recover from mid-run failure by rehydrating state from checkpoint.

Deliverables:
- results/stage6/topic03_memory_checkpoint.json
- results/stage6/topic03_memory_recovery_report.csv
"""

from __future__ import annotations

import json
from pathlib import Path

from stage6_utils import RESULTS_DIR, print_data_declaration


def retrieve_top_memory(query: str, memory_store: list[dict[str, str]], top_k: int = 2) -> list[dict[str, str]]:
    """Simple overlap-based memory retrieval for educational clarity."""
    q_tokens = set(query.lower().split())
    scored = []
    for record in memory_store:
        tokens = set(record["text"].lower().split())
        overlap = len(q_tokens & tokens)
        scored.append((overlap, record))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]]


def save_checkpoint(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def load_checkpoint(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    lines = [",".join(fields)]
    for row in rows:
        lines.append(",".join(str(row[f]).replace(",", ";") for f in fields))
    path.write_text("\n".join(lines), encoding="utf-8")


# Workflow:
# 1) Build memory store and initial query.
# 2) Run retrieval and persist checkpoint.
# 3) Simulate failure before response-generation step.
# 4) Reload checkpoint and continue from failed step (time-travel debug pattern).
def main() -> None:
    print_data_declaration("Topic03 Memory Retrieval Intermediate (Checkpointing)")

    memory_store = [
        {"id": "M1", "text": "Enterprise outages need severity rubric and fast escalation."},
        {"id": "M2", "text": "Billing disputes require invoice evidence and contract check."},
        {"id": "M3", "text": "Security incidents require identity verification before disclosure."},
        {"id": "M4", "text": "Ontario subdivision GeoJSON is sensitive and cannot be sent externally."},
    ]
    query = "customer reports security alert and suspicious access in Ontario subdivision system"

    out_dir = Path(RESULTS_DIR) / "stage6"
    checkpoint_path = out_dir / "topic03_memory_checkpoint.json"
    recovery_report_path = out_dir / "topic03_memory_recovery_report.csv"

    # Step 1: initial run state.
    state = {
        "run_id": "stage6_topic03_memory_checkpoint_demo",
        "step_index": 1,
        "query": query,
        "retrieved_memory_ids": [],
        "status": "running",
        "failure_class": None,
    }
    save_checkpoint(checkpoint_path, state)

    # Step 2: retrieve memory, then checkpoint.
    top_records = retrieve_top_memory(query, memory_store, top_k=2)
    state["step_index"] = 2
    state["retrieved_memory_ids"] = [r["id"] for r in top_records]
    save_checkpoint(checkpoint_path, state)

    print("\nQuery:")
    print(query)
    print("\nRetrieved memory records:")
    for rec in top_records:
        print(f"- {rec['id']}: {rec['text']}")

    # Step 3: simulate failure before completion.
    state["step_index"] = 3
    state["status"] = "failed"
    state["failure_class"] = "simulated_runtime_failure_at_step_3"
    save_checkpoint(checkpoint_path, state)
    print("\nSimulated failure occurred at step 3. Checkpoint saved.")

    # Step 4: recover from checkpoint and finish from failed step.
    restored = load_checkpoint(checkpoint_path)
    resumed_from = restored["step_index"]

    # Resume logic: rehydrate state then continue remaining steps only.
    restored["step_index"] = 4
    restored["status"] = "completed_after_resume"
    restored["final_summary"] = (
        "Recovered from checkpoint; response can proceed using retrieved memory IDs "
        + ", ".join(restored["retrieved_memory_ids"])
    )
    save_checkpoint(checkpoint_path, restored)

    print("Resumed from checkpoint step:", resumed_from)
    print("Final status:", restored["status"])
    print("Final summary:", restored["final_summary"])

    rows = [
        {
            "run_id": restored["run_id"],
            "resumed_from_step": resumed_from,
            "resume_success": True,
            "failure_class": state["failure_class"],
            "final_status": restored["status"],
            "retrieved_memory_count": len(restored["retrieved_memory_ids"]),
        }
    ]
    write_csv(recovery_report_path, rows)

    print("\nSaved artifacts:")
    print(f"- {checkpoint_path}")
    print(f"- {recovery_report_path}")
    print("\nReliability note:")
    print("- Checkpointing prevents full restart in long-running agent workflows.")


if __name__ == "__main__":
    main()

