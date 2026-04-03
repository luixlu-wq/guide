"""Stage 3 Topic 06 (Advanced): K selection with inertia/silhouette/ARI.

Data: sklearn.datasets.make_blobs
Rows: 1200
Features: 6 numeric
Target: true cluster id (used only for validation metric ARI)
Type: Clustering (advanced evaluation)
"""

from __future__ import annotations

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
    print("Interpretation: real projects usually use inertia/silhouette; ARI is only available when true labels exist.")


if __name__ == "__main__":
    main()

