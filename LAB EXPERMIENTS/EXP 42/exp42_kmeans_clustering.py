from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# 1. Generate sample data (4 distinct groups)
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# 2. Implement K-Means Clustering Algorithm
kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

print("Cluster Centers:\n", kmeans.cluster_centers_)
print("First 10 Labels:\n", y_kmeans[:10])

# Optional Plotting (Uncomment to visualize if running locally)
# plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
# plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', s=200, alpha=0.75, marker='X')
# plt.title("K-Means Clustering")
# plt.show()
