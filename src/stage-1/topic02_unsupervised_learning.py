import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler


def load_data():
    X, y_true = load_iris(return_X_y=True)
    return X, y_true


def run_kmeans(X, n_clusters=3):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)
    return X_scaled, labels


def main():
    X, y_true = load_data()
    X_scaled, labels = run_kmeans(X, n_clusters=3)

    sil = silhouette_score(X_scaled, labels)
    ari = adjusted_rand_score(y_true, labels)

    print("silhouette score:", round(sil, 4))
    print("adjusted rand index:", round(ari, 4))
    print("cluster counts:", np.bincount(labels))


if __name__ == "__main__":
    main()
