from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

# Generate reproducible sample data.
X, _ = make_blobs(
    n_samples=300,
    centers=4,
    cluster_std=0.60,
    random_state=42,
)

# Train and evaluate K-Means.
kmeans = KMeans(n_clusters=4, n_init=20, random_state=42)
labels = kmeans.fit_predict(X)

print("Cluster Centers:")
print(kmeans.cluster_centers_)
print("First 10 Labels:", labels[:10])
print(f"Inertia: {kmeans.inertia_:.2f}")
print(f"Silhouette Score: {silhouette_score(X, labels):.4f}")
