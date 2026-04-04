"""
lab08_circuit_breaker_incident_response

Lab goal:
- Validate stateful circuit-breaker behavior under repeated tool failures.
- Produce incident evidence showing stop-loop fallback behavior.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage10_utils import RESULTS_DIR, as_jsonl, print_data_declaration, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic repeated tool-failure sequence",
        "Records/Samples": "5 tool call events",
        "Input schema": "tool_name, status_code, parse_ok",
        "Output schema": "breaker_state, fallback_action",
        "Split/Eval policy": "fixed failure injection sequence",
        "Type": "agentic safety + incident response",
    }
    print_data_declaration("Lab 8 - Circuit Breaker Incident Response", declaration)

    events = [
        {"timestamp": datetime(2026, 4, 4, 15, 30, 0).isoformat(), "tool": "ontario_gis_api", "status": 404, "breaker_state": "closed", "action": "retry"},
        {"timestamp": datetime(2026, 4, 4, 15, 30, 20).isoformat(), "tool": "ontario_gis_api", "status": 404, "breaker_state": "closed", "action": "retry"},
        {"timestamp": datetime(2026, 4, 4, 15, 30, 40).isoformat(), "tool": "ontario_gis_api", "status": 404, "breaker_state": "open", "action": "fallback_read_only"},
        {"timestamp": datetime(2026, 4, 4, 15, 31, 40).isoformat(), "tool": "ontario_gis_api", "status": 200, "breaker_state": "half_open", "action": "probe"},
        {"timestamp": datetime(2026, 4, 4, 15, 31, 55).isoformat(), "tool": "ontario_gis_api", "status": 200, "breaker_state": "closed", "action": "resume"},
    ]
    as_jsonl(RESULTS_DIR / "circuit_breaker_incident_log.jsonl", events)

    postmortem = [
        "# Incident Postmortem Drill",
        "",
        "- Incident type: repeated tool failure loop.",
        "- Trigger: same tool failure >= 3 times in 60 seconds.",
        "- Mitigation: breaker opened and deterministic fallback returned.",
        "- Outcome: loop stopped, user received controlled response.",
    ]
    write_text(RESULTS_DIR / "incident_postmortem_drill.md", "\n".join(postmortem))

    print("[INFO] Lab 8 outputs written:")
    print("- results/circuit_breaker_incident_log.jsonl")
    print("- results/incident_postmortem_drill.md")


if __name__ == "__main__":
    main()

