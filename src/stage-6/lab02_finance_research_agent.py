"""Stage 6 Lab 02: Finance research agent (offline deterministic demo).

Deliverables:
- results/lab2_outputs.jsonl
- results/lab2_grounding_report.md
- results/lab2_comparison_before_after.csv
"""

from __future__ import annotations

from pathlib import Path

from stage6_utils import RESULTS_DIR, as_csv, as_jsonl, print_data_declaration


print_data_declaration("Lab02 Finance Research Agent")

research_notes = [
    {"id": "N1", "symbol": "NVDA", "note": "Revenue growth remains strong; supply constraints easing."},
    {"id": "N2", "symbol": "AAPL", "note": "Services margin stable; hardware cycle mixed."},
    {"id": "N3", "symbol": "MSFT", "note": "Cloud demand remains resilient with AI workload expansion."},
]


def analytics_tool(symbol: str) -> dict:
    """Deterministic toy analytics output for reproducible teaching."""
    values = {
        "NVDA": {"momentum_30d": 0.18, "volatility_30d": 0.31},
        "AAPL": {"momentum_30d": 0.06, "volatility_30d": 0.16},
        "MSFT": {"momentum_30d": 0.09, "volatility_30d": 0.14},
    }
    return values[symbol]


# Baseline: summary from notes only.
baseline = []
for row in research_notes:
    baseline.append(
        {
            "symbol": row["symbol"],
            "summary": f"Baseline summary: {row['note']}",
            "citations": [row["id"]],
            "grounded": True,
        }
    )

# Improved: summary uses note + analytics tool.
improved = []
for row in research_notes:
    stats = analytics_tool(row["symbol"])
    improved.append(
        {
            "symbol": row["symbol"],
            "summary": (
                f"Improved summary: {row['note']} "
                f"Momentum={stats['momentum_30d']:.2f}, Volatility={stats['volatility_30d']:.2f}."
            ),
            "citations": [row["id"], f"ANALYTICS-{row['symbol']}"] ,
            "grounded": True,
        }
    )

# Save improved outputs.
outputs_path = Path(RESULTS_DIR) / "lab2_outputs.jsonl"
as_jsonl(outputs_path, improved)

# Save grounding report.
grounding_report = [
    "# Lab2 Grounding Report",
    "",
    "All outputs include note citation IDs and analytics source tags.",
    "No ungrounded claims were intentionally generated in this deterministic demo.",
]
report_path = Path(RESULTS_DIR) / "lab2_grounding_report.md"
report_path.write_text("\n".join(grounding_report), encoding="utf-8")

# Save before/after comparison metrics.
comparison_rows = [
    {"label": "baseline", "citation_count_avg": 1.0, "tool_usage_rate": 0.0},
    {"label": "improved", "citation_count_avg": 2.0, "tool_usage_rate": 1.0},
]
comparison_path = Path(RESULTS_DIR) / "lab2_comparison_before_after.csv"
as_csv(comparison_path, comparison_rows)

print("\nLab02 completed. Deliverables:")
print(f"- {outputs_path}")
print(f"- {report_path}")
print(f"- {comparison_path}")
