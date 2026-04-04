"""Stage 7 Topic 01C: Chunk quality diagnostics (advanced)."""

from __future__ import annotations

from stage7_utils import ensure_stage7_dataset, load_docs, print_data_declaration


print_data_declaration("Topic01C Chunk Quality Advanced", "chunk diagnostics")
ensure_stage7_dataset()
docs = load_docs()

print("\n=== Diagnostic checks ===")

# Check 1: overly short chunks are often weak retrieval evidence.
short_chunks = [d for d in docs if len(d.text) < 50]
print(f"short_chunk_count={len(short_chunks)}")

# Check 2: missing source or section breaks citation traceability.
missing_meta = [d for d in docs if (not d.source) or (not d.section)]
print(f"missing_metadata_count={len(missing_meta)}")

# Check 3: duplicate text can cause redundancy and unstable ranking.
seen = set()
duplicates = 0
for d in docs:
    key = d.text.strip().lower()
    if key in seen:
        duplicates += 1
    seen.add(key)
print(f"duplicate_chunk_count={duplicates}")

print("\nInterpretation:")
print("- short chunks may lose context")
print("- missing metadata harms citations")
print("- duplicates add retrieval noise")
