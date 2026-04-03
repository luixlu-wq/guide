"""Stage 3 Topic 06 (Simple): KMeans on simple blobs.

Data: sklearn.datasets.make_blobs
Rows: 300
Features: 2 numeric
Target: optional labels for validation only
Type: Clustering (simple)
"""

from __future__ import annotations

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score


# Workflow:
# 1) Generate simple blob clusters.
# 2) Fit KMeans with fixed K.
# 3) Print inertia, silhouette, and cluster centers.
def main() -> None:
    X, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.8, random_state=42)

    model = KMeans(n_clusters=3, random_state=42, n_init=20)
    labels = model.fit_predict(X)

    print("Data source: make_blobs")
    print("Rows: 300, Features: 2")
    print("Inertia:", round(model.inertia_, 2))
    print("Silhouette:", round(silhouette_score(X, labels), 3))
    print("Centers:")
    print(model.cluster_centers_)


if __name__ == "__main__":
    main()

