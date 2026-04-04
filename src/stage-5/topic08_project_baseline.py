"""Stage 5 Topic 08: practice project baseline (operatable, file outputs).

Data: fixed in-script JSON-like records
Records/Samples: 24
Input schema: id, text
Output schema: structured JSON fields + metrics tables
Split/Eval policy: fixed dev/test split by index
Type: Stage 5 project baseline
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import json
import pandas as pd

from stage5_utils import mock_llm, try_parse_json, validate_schema


def run_prompt_version(records: list[dict[str, str]], mode: str) -> tuple[list[dict], list[dict]]:
    rows = []
    raw_lines = []
    for row in records:
        raw = mock_llm(row["text"], mode)
        obj, err = try_parse_json(raw)
        parse_ok = obj is not None
        schema_ok = False
        if parse_ok:
            schema_ok, _ = validate_schema(obj)
        rows.append(
            {
                "id": row["id"],
                "mode": mode,
                "parse_ok": int(parse_ok),
                "schema_ok": int(schema_ok),
            }
        )
        raw_lines.append({"id": row["id"], "mode": mode, "raw_output": raw, "parse_error": err})
    return rows, raw_lines


def build_dataset() -> list[dict[str, str]]:
    base = [
        "Revenue grew but regulatory investigation increased uncertainty.",
        "Launch delay risk increased due to supplier shortage.",
        "Margin pressure rose with debt refinancing costs.",
        "Security review added compliance overhead.",
        "Guidance remained cautious because of volatility.",
        "Product recall created legal and reputational risk.",
    ]
    data = []
    idx = 1
    for _ in range(4):
        for t in base:
            data.append({"id": f"r{idx:02d}", "text": t})
            idx += 1
    return data


# Workflow:
# 1) Run baseline prompt mode (json_weak) and collect outputs.
# 2) Run improved prompt mode (json_strong) on same split.
# 3) Export before/after metrics and reproducibility files.
def main() -> None:
    records = build_dataset()
    dev = records[:12]
    test = records[12:]

    print("Data declaration")
    print("source=in_script_project_dataset")
    print(f"records={len(records)} dev={len(dev)} test={len(test)}")
    print("input_schema={id:str,text:str}")
    print("output_schema={summary,risks,citations}")

    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(exist_ok=True)

    before_rows_dev, before_raw_dev = run_prompt_version(dev, "json_weak")
    after_rows_dev, after_raw_dev = run_prompt_version(dev, "json_strong")

    before_rows_test, before_raw_test = run_prompt_version(test, "json_weak")
    after_rows_test, after_raw_test = run_prompt_version(test, "json_strong")

    before_df = pd.DataFrame(before_rows_dev + before_rows_test)
    after_df = pd.DataFrame(after_rows_dev + after_rows_test)

    before_metrics = {
        "parse_rate": float(before_df["parse_ok"].mean()),
        "schema_rate": float(before_df["schema_ok"].mean()),
    }
    after_metrics = {
        "parse_rate": float(after_df["parse_ok"].mean()),
        "schema_rate": float(after_df["schema_ok"].mean()),
    }

    pd.DataFrame([before_metrics]).to_csv(results_dir / "metrics_before.csv", index=False)
    pd.DataFrame([after_metrics]).to_csv(results_dir / "metrics_after.csv", index=False)

    with (results_dir / "raw_outputs_before.jsonl").open("w", encoding="utf-8") as f:
        for row in before_raw_dev + before_raw_test:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with (results_dir / "raw_outputs_after.jsonl").open("w", encoding="utf-8") as f:
        for row in after_raw_dev + after_raw_test:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    validity_report = {
        "before": before_metrics,
        "after": after_metrics,
        "delta_schema_rate": after_metrics["schema_rate"] - before_metrics["schema_rate"],
    }
    (results_dir / "format_validity_report.json").write_text(
        json.dumps(validity_report, indent=2), encoding="utf-8"
    )

    (results_dir / "hallucination_audit.md").write_text(
        "# Hallucination Audit\n\n"
        "This offline baseline focuses on structure reliability.\n"
        "For factual grounding audit, connect retrieval context and citation checks in next iteration.\n",
        encoding="utf-8",
    )

    (results_dir / "final_prompt_selection.md").write_text(
        "# Final Prompt Selection\n\n"
        f"Selected: json_strong\n\n"
        f"Reason: schema_rate improved from {before_metrics['schema_rate']:.3f} to {after_metrics['schema_rate']:.3f}.\n",
        encoding="utf-8",
    )

    (results_dir / "reproducibility.md").write_text(
        "# Reproducibility\n\n"
        "- Dataset: in-script fixed 24 records\n"
        "- Split: first 12 dev, last 12 test\n"
        "- Prompt versions: json_weak vs json_strong\n"
        f"- Run date: {date.today().isoformat()}\n",
        encoding="utf-8",
    )

    print(f"metrics_before={before_metrics}")
    print(f"metrics_after={after_metrics}")
    print(f"results_dir={results_dir}")
    print("Interpretation: project comparison must use fixed data and versioned prompts.")


if __name__ == "__main__":
    main()
