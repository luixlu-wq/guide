"""Stage 3 Topic 06: KMeans clustering and silhouette-based K selection.

Data: sklearn.datasets.load_iris (features only)
Rows: 150
Features: 4 numeric features
Target: not used during training (unsupervised)
Type: Clustering
"""

from __future__ import annotations

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

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    best_k = None
    best_score = -1.0

    for k in range(2, 7):
        model = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        print(f"k={k}, silhouette={score:.3f}")
        if score > best_score:
            best_score = score
            best_k = k

    final_model = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    final_labels = final_model.fit_predict(X_scaled)
    counts = np.bincount(final_labels)

    print("Best k:", best_k)
    print("Cluster sizes:", counts.tolist())
    print("Interpretation: KMeans groups by distance and requires K selection.")


if __name__ == "__main__":
    main()

