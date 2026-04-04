"""
lab02_incident_command_drill

Lab goal:
- Execute incident command process and create postmortem artifacts.
"""

from __future__ import annotations

from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage16_utils import RESULTS_DIR, print_data_declaration, write_rows_csv, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic incident command drill",
        "Requests/Samples": "1 incident",
        "Input schema": "time, role, action, status",
        "Output schema": "timeline and postmortem",
        "Eval policy": "fixed incident script",
        "Type": "incident_command",
    }
    print_data_declaration("Lab 2 - Incident Command Drill", declaration)

    timeline = [
        {"minute": 0, "role": "incident_commander", "action": "declare_sev2", "status": "done"},
        {"minute": 5, "role": "tech_owner", "action": "stabilize_service", "status": "done"},
        {"minute": 14, "role": "comms_owner", "action": "stakeholder_update", "status": "done"},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_incident_timeline.csv", timeline)

    owners = [
        {"action": "root_cause_analysis", "owner": "tech_owner"},
        {"action": "mitigation_validation", "owner": "incident_commander"},
        {"action": "postmortem_publish", "owner": "comms_owner"},
    ]
    write_rows_csv(RESULTS_DIR / "lab2_actions_and_owners.csv", owners)

    write_text(
        RESULTS_DIR / "lab2_postmortem.md",
        "# Lab 2 Postmortem\n\n- Incident resolved in 23 minutes.\n- Key lesson: clearer freshness alert threshold reduced detection delay.\n",
    )


if __name__ == "__main__":
    main()
