"""Stage 6 Topic 09C: Incident response advanced.

This script simulates one security incident, applies a targeted fix, and writes
an incident postmortem artifact.
"""

from pathlib import Path

from stage6_utils import RESULTS_DIR, print_data_declaration, summarize_incident


print_data_declaration("Topic09C Incident Response Advanced")

case_id = "INC-2026-0404-01"
failure = "prompt_injection_bypassed_policy_gate"
fix = "enforce_argument_allowlist_and_block_sensitive_export_tools"
outcome = "attack_blocked_in_rerun; no data exfiltration"

postmortem_text = summarize_incident(case_id, failure, fix, outcome)

output_path = Path(RESULTS_DIR) / "topic09_incident_postmortem.md"
output_path.write_text(postmortem_text, encoding="utf-8")

print("\n=== Incident Postmortem ===")
print(postmortem_text)
print(f"saved_to={output_path}")

print("\nAdvanced note:")
print("- Incident handling must produce artifacts for audit and learning loops.")
