"""Stage 7 Topic 06A: Index freshness (simple)."""

from __future__ import annotations

import json
from pathlib import Path

from stage7_utils import DATA_DIR, ensure_stage7_dataset, load_docs, now_ts, print_data_declaration

print_data_declaration("Topic06A Index Freshness Simple", "operations/freshness")
ensure_stage7_dataset()
docs = load_docs()

freshness_log = Path(DATA_DIR) / "index_sync_log_stage7.json"

latest_update = max(d.updated_at for d in docs)
state = {
    "last_sync_at": now_ts(),
    "latest_document_update": latest_update,
    "document_count": len(docs),
    "status": "sync_completed",
}
freshness_log.write_text(json.dumps(state, indent=2), encoding="utf-8")

print("\nindex_sync_state=", state)
print(f"sync_log_path={freshness_log}")
