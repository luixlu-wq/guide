"""Stage 3 Topic 06: KMeans clustering and silhouette-based K selection.

Data Source: sklearn.datasets.load_iris (features only)
Schema: 4 numeric features | Target unused for training (unsupervised)
Preprocessing: StandardScaler required for distance-based clustering reliability
Null Handling: None (dataset is verified clean by source package)
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


# Workflow:
# 1) Scale iris features for distance-based clustering.
# 2) Sweep K values and compute silhouette score.
# 3) Select best K and print cluster sizes.
def main() -> None:
    data = load_iris(as_frame=True)
    X = data.data

    print("Data source: sklearn.datasets.load_iris")
    print(f"Rows: {X.shape[0]}")
    print(f"Features: {X.shape[1]}")
    print("Target is ignored in KMeans training.")
    print("Scaling check: KMeans distance geometry breaks if features are not standardized.")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    best_k = None
    best_score = -1.0
    rows = []

    for k in range(2, 7):
        model = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        inertia = float(model.inertia_)
        rows.append({"k": k, "silhouette": float(score), "inertia": inertia})
        print(f"k={k}, silhouette={score:.3f}, inertia={inertia:.3f}")
        if score > best_score:
            best_score = score
            best_k = k

    final_model = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    final_labels = final_model.fit_predict(X_scaled)
    counts = np.bincount(final_labels)

    print("Best k:", best_k)
    print("Cluster sizes:", counts.tolist())
    if best_score < 0.4:
        print("DIAGNOSIS: Weak separation. Revisit features or consider different clustering methods.")
    else:
        print("DIAGNOSIS: Cluster separation is acceptable for a baseline.")

    out_dir = Path(__file__).parent / "results" / "stage3"
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows).sort_values("silhouette", ascending=False)
    df.to_csv(out_dir / "topic06_kmeans_k_scan.csv", index=False)
    (out_dir / "topic06_kmeans_k_scan.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    print(f"Saved: {out_dir / 'topic06_kmeans_k_scan.csv'}")
    print(f"Saved: {out_dir / 'topic06_kmeans_k_scan.json'}")
    print("Interpretation: KMeans groups by distance and requires K selection.")


if __name__ == "__main__":
    main()

