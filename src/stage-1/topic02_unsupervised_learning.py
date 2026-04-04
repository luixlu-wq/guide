"""Topic 02: Unsupervised clustering baseline with structured artifact output."""

from __future__ import annotations

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

from common.runtime import create_logger, write_json_artifact


def main() -> None:
    script_stem = "topic02_unsupervised_learning"
    logger = create_logger(script_stem)

    X, y_true = load_iris(return_X_y=True)
    X_scaled = StandardScaler().fit_transform(X)
    labels = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X_scaled)

    sil = float(silhouette_score(X_scaled, labels))
    ari = float(adjusted_rand_score(y_true, labels))
    cluster_counts = np.bincount(labels).tolist()

    logger.info("silhouette_score=%.4f adjusted_rand_index=%.4f", sil, ari)
    logger.info("cluster_counts=%s", cluster_counts)

    artifact_path = write_json_artifact(
        script_stem,
        "metrics",
        {
            "dataset": "iris",
            "input_rows_or_samples": int(X.shape[0]),
            "quality_metric_name": "silhouette_score",
            "quality_metric_value": sil,
            "metrics": {
                "silhouette_score": sil,
                "adjusted_rand_index": ari,
                "cluster_counts": cluster_counts,
            },
            "decision_note": "baseline unsupervised clustering run",
        },
    )
    logger.info("artifact_saved=%s", artifact_path)


if __name__ == "__main__":
    main()
