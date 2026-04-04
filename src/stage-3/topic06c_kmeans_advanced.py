"""Stage 3 Topic 06 (Advanced): K selection with inertia/silhouette/ARI.

Data Source: sklearn.datasets.make_blobs
Schema: 6 numeric features | Target true cluster id (validation only)
Preprocessing: StandardScaler required for fair distance comparisons
Null Handling: None (synthetic generator produces complete arrays)
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler


# Workflow:
# 1) Generate higher-dimensional blob clusters and scale features.
# 2) Evaluate multiple K values with inertia and silhouette.
# 3) Add ARI (with known labels) as advanced validation signal.
def main() -> None:
    print("Scaling check: distance metrics (inertia/silhouette) require standardized features.")
    X, y_true = make_blobs(
        n_samples=1200,
        centers=4,
        n_features=6,
        cluster_std=1.1,
        random_state=42,
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    rows = []
    for k in range(2, 8):
        model = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(X_scaled)

        rows.append(
            {
                "k": k,
                "inertia": model.inertia_,
                "silhouette": silhouette_score(X_scaled, labels),
                "ari_vs_true": adjusted_rand_score(y_true, labels),
            }
        )

    df = pd.DataFrame(rows).sort_values("silhouette", ascending=False)
    print("Data source: make_blobs (with known clusters for validation)")
    print("Rows: 1200, Features: 6")
    print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    out_dir = Path(__file__).parent / "results" / "stage3"
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "topic06c_kmeans_advanced_metrics.csv", index=False)
    (out_dir / "topic06c_kmeans_advanced_metrics.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    print(f"Saved: {out_dir / 'topic06c_kmeans_advanced_metrics.csv'}")
    print(f"Saved: {out_dir / 'topic06c_kmeans_advanced_metrics.json'}")
    print("Interpretation: real projects usually use inertia/silhouette; ARI is only available when true labels exist.")


if __name__ == "__main__":
    main()

