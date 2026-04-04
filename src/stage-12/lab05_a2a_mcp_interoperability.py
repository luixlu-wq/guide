"""
lab05_a2a_mcp_interoperability

Lab goal:
- Demonstrate A2A-style discovery/handoff traces with agent cards.
- Demonstrate MCP-style tool contract standardization.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage12_utils import RESULTS_DIR, as_jsonl, print_data_declaration, write_json, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic inter-agent capability registry and handoff events",
        "Requests/Samples": "2 agents + 4 handoff events",
        "Input schema": "agent_id, capability_tags, handoff_request",
        "Output schema": "agent_cards, handoff_trace, tool_contracts",
        "Eval policy": "fixed orchestration simulation",
        "Type": "a2a + mcp interoperability",
    }
    print_data_declaration("Lab 5 - A2A MCP Interoperability", declaration)

    agent_cards = {
        "agents": [
            {
                "agent_id": "gis_validation_agent",
                "display_name": "Ontario GIS Validation Agent",
                "capabilities": ["projection_check", "geojson_schema_validation"],
                "trust_boundary": "internal",
            },
            {
                "agent_id": "tour_planning_agent",
                "display_name": "MapToGo Tour Planning Agent",
                "capabilities": ["poi_ranking", "itinerary_generation"],
                "trust_boundary": "internal",
            },
        ]
    }
    write_json(RESULTS_DIR / "agent_card_registry.json", agent_cards)

    handoffs = [
        {
            "timestamp": datetime(2026, 4, 4, 16, 0, 0).isoformat(),
            "trace_id": "a2a_001",
            "from_agent": "tour_planning_agent",
            "to_agent": "gis_validation_agent",
            "task": "validate_coordinates",
            "status": "accepted",
        },
        {
            "timestamp": datetime(2026, 4, 4, 16, 0, 1).isoformat(),
            "trace_id": "a2a_001",
            "from_agent": "gis_validation_agent",
            "to_agent": "tour_planning_agent",
            "task": "return_projection_check",
            "status": "completed",
        },
    ]
    as_jsonl(RESULTS_DIR / "a2a_handoff_trace.jsonl", handoffs)

    mcp_contract = [
        "# MCP Tool Contracts",
        "",
        "## tool: validate_geojson_projection",
        "- input: `{geojson: object, expected_crs: string}`",
        "- output: `{ok: bool, detected_crs: string, issues: list}`",
        "- safety: reject if mandatory coordinates are missing",
        "",
        "## tool: rank_poi_candidates",
        "- input: `{poi_list: array, preference_profile: object}`",
        "- output: `{ranked_poi: array, score_breakdown: object}`",
        "- safety: redact sensitive admin identifiers before external calls",
    ]
    write_text(RESULTS_DIR / "mcp_tool_contracts.md", "\n".join(mcp_contract))

    print("[INFO] Lab 5 outputs written:")
    print("- results/agent_card_registry.json")
    print("- results/a2a_handoff_trace.jsonl")
    print("- results/mcp_tool_contracts.md")


if __name__ == "__main__":
    main()

