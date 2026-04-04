"""
topic11c_synthetic_data_governance_advanced

Advanced synthetic-data governance:
- generate synthetic dataset
- run dedupe + quality checks
- export canonical artifact: results/stage8/synthetic_data_curation_report.md
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from stage8_utils import STAGE8_RESULTS_DIR, print_data_declaration, write_text


def main() -> None:
    declaration = {
        "Data": "Synthetic self-instruct style dataset",
        "Records": "1000 raw generated",
        "Input schema": "instruction, input_context",
        "Output schema": "target_response",
        "Split/Eval policy": "fixed deterministic generation/filter policy",
        "Type": "synthetic data governance advanced",
    }
    print_data_declaration("Topic11C Synthetic Data Governance Advanced", declaration)

    raw = []
    for i in range(1000):
        instr = [
            "Generate Ontario subdivision safety summary",
            "Create citation-grounded GIS response",
            "Format policy-safe trend/risk/reason JSON",
        ][i % 3]
        # Intentional duplicates and short outputs for governance checks.
        input_ctx = f"ontario_subdivision_case_{i if i % 11 else 0}"
        output = (
            "trend=neutral; risk=medium; reason=insufficient evidence, cite authoritative source."
            if i % 23 != 0
            else "n/a"
        )
        raw.append({"instruction": instr, "input": input_ctx, "output": output})

    # Dedupe.
    seen = set()
    deduped = []
    for r in raw:
        k = (r["instruction"], r["input"], r["output"])
        if k in seen:
            continue
        seen.add(k)
        deduped.append(r)

    # Quality checks.
    min_len_threshold = 24
    curated = [r for r in deduped if len(r["output"]) >= min_len_threshold]
    rejected = [r for r in deduped if len(r["output"]) < min_len_threshold]
    acceptance_rate = round(len(curated) / max(len(raw), 1), 4)

    report = [
        "# Synthetic Data Curation Report",
        "",
        f"generated_at: {datetime.now(timezone.utc).isoformat()}",
        "dataset_version: synthetic_v1",
        "",
        "## Volume",
        f"- raw_count: {len(raw)}",
        f"- deduped_count: {len(deduped)}",
        f"- curated_count: {len(curated)}",
        f"- rejected_count: {len(rejected)}",
        f"- acceptance_rate: {acceptance_rate}",
        "",
        "## Governance checks",
        f"- min_output_length_threshold: {min_len_threshold}",
        "- dedupe_policy: exact tuple dedupe on instruction/input/output",
        "- quality_policy: reject low-information outputs",
        "",
        "## Samples (curated)",
    ]
    for s in curated[:3]:
        report.append(f"- instruction={s['instruction']} | input={s['input']} | output={s['output']}")

    out = STAGE8_RESULTS_DIR / "synthetic_data_curation_report.md"
    write_text(out, "\n".join(report))
    print(f"[INFO] Wrote: {out}")


if __name__ == "__main__":
    main()

